"""
Harbor agent adapter for the lightningrod-assistant Claude Code agent.

Uses the Claude Agent SDK to run the agent and capture the full conversation
trajectory in ATIF format. Writes both trajectory.json (full trace) and
response.txt (final output, for backward-compatible verifiers).
"""

import asyncio
import base64
import json
from datetime import datetime, timezone
from pathlib import Path

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, ResultMessage
from claude_agent_sdk.types import (
    AssistantMessage, UserMessage, TextBlock, ThinkingBlock,
    ToolUseBlock, ToolResultBlock,
)

from harbor.agents.base import BaseAgent
from harbor.environments.base import BaseEnvironment
from harbor.models.agent.context import AgentContext

# Repo root on the host — agent needs this as cwd for .claude/ directory access
SDK_ROOT = Path(__file__).resolve().parent.parent


class LightningrodAssistantAgent(BaseAgent):
    """Wraps the lightningrod-assistant Claude Code agent for Harbor evaluation."""

    AGENT_NAME = "lightningrod-assistant"
    SUPPORTS_ATIF = True
    MAX_TURNS = 5

    @staticmethod
    def name() -> str:
        return "lightningrod-assistant"

    def version(self) -> str | None:
        return "2.0.0"

    async def setup(self, environment: BaseEnvironment) -> None:
        pass

    async def run(
        self,
        instruction: str,
        environment: BaseEnvironment,
        context: AgentContext,
    ) -> None:
        self.logger.info(f"Running agent via SDK with cwd={SDK_ROOT}")

        opts = ClaudeAgentOptions(
            extra_args={"agent": self.AGENT_NAME},
            cwd=SDK_ROOT,
            permission_mode="bypassPermissions",
            max_turns=self.MAX_TURNS,
            disallowed_tools=["AskUserQuestion"],
        )

        trajectory: list = []
        result_msg: ResultMessage | None = None

        try:
            async with ClaudeSDKClient(options=opts) as client:
                await client.query(instruction)
                async for msg in client.receive_response():
                    trajectory.append(msg)
                    if isinstance(msg, ResultMessage):
                        result_msg = msg
        except Exception as e:
            error_text = f"[AGENT ERROR] SDK execution failed: {e}"
            self.logger.error(error_text)
            await self._write_to_container(environment, "response.txt", error_text)
            await self._write_to_container(environment, "trajectory.json", json.dumps(
                {"error": str(e), "steps": []}, indent=2
            ))
            context.metadata = {"error": str(e)}
            return

        # Convert to ATIF and extract final response
        atif = _trajectory_to_atif(trajectory, result_msg)
        final_response = (result_msg.result if result_msg else None) or ""

        if not final_response:
            final_response = "[AGENT ERROR] No output"

        # Write both files to the container
        await self._write_to_container(environment, "response.txt", final_response)
        await self._write_to_container(
            environment, "trajectory.json", json.dumps(atif, indent=2)
        )

        # Set Harbor context metrics
        if result_msg:
            usage = result_msg.usage or {}
            context.cost_usd = result_msg.total_cost_usd
            context.n_input_tokens = usage.get("input_tokens", 0)
            context.n_output_tokens = usage.get("output_tokens", 0)
            context.n_cache_tokens = usage.get("cache_read_input_tokens", 0)

        context.metadata = {
            "response_length": len(final_response),
            "num_turns": result_msg.num_turns if result_msg else 0,
            "tools_used": atif.get("agent", {}).get("tools_used", []),
        }

    async def _write_to_container(
        self, environment: BaseEnvironment, filename: str, content: str,
    ) -> None:
        """Write a file into the container's /logs/agent/ directory."""
        await environment.exec("mkdir -p /logs/agent", timeout_sec=10)
        encoded = base64.b64encode(content.encode()).decode()
        await environment.exec(
            f"echo '{encoded}' | base64 -d > /logs/agent/{filename}",
            timeout_sec=10,
        )


def _trajectory_to_atif(
    messages: list, result_msg: ResultMessage | None,
) -> dict:
    """Convert SDK messages to ATIF trajectory dict."""
    steps: list[dict] = []
    step_id = 0
    now = datetime.now(timezone.utc).isoformat()
    pending: dict[str, ToolUseBlock] = {}
    tools_used: set[str] = set()

    def _step(source: str, message: str, **kw) -> dict:
        nonlocal step_id
        step_id += 1
        s = {"step_id": step_id, "timestamp": now, "source": source, "message": message}
        s.update({k: v for k, v in kw.items() if v is not None})
        return s

    for msg in messages:
        if isinstance(msg, UserMessage):
            if isinstance(msg.content, list):
                all_tool_results = True
                for b in msg.content:
                    if isinstance(b, ToolResultBlock) and b.tool_use_id in pending:
                        tu = pending.pop(b.tool_use_id)
                        tools_used.add(tu.name)
                        content = (
                            b.content if isinstance(b.content, str)
                            else json.dumps(b.content) if b.content else ""
                        )
                        steps.append(_step(
                            "agent", f"Tool: {tu.name}",
                            tool_calls=[{
                                "tool_call_id": tu.id,
                                "function_name": tu.name,
                                "arguments": tu.input,
                            }],
                            observation={"results": [{
                                "source_call_id": tu.id,
                                "content": content,
                            }]},
                        ))
                    else:
                        all_tool_results = False
                if all_tool_results:
                    continue
            text = msg.content if isinstance(msg.content, str) else str(msg.content)
            if text:
                steps.append(_step("user", text))

        elif isinstance(msg, AssistantMessage):
            texts: list[str] = []
            reasoning: str | None = None
            for b in msg.content:
                if isinstance(b, TextBlock):
                    texts.append(b.text)
                elif isinstance(b, ThinkingBlock):
                    reasoning = b.thinking
                elif isinstance(b, ToolUseBlock):
                    pending[b.id] = b
            if texts or reasoning:
                steps.append(_step(
                    "agent", "\n".join(texts) or "(thinking)",
                    reasoning_content=reasoning,
                    model_name=getattr(msg, "model", None),
                ))

    # Flush any pending tool calls that never got results
    for tu in pending.values():
        tools_used.add(tu.name)
        steps.append(_step(
            "agent", f"Tool: {tu.name}",
            tool_calls=[{
                "tool_call_id": tu.id,
                "function_name": tu.name,
                "arguments": tu.input,
            }],
        ))

    if not steps:
        steps.append(_step("user", "(empty)"))

    # Final metrics
    final_metrics = None
    if result_msg:
        usage = result_msg.usage or {}
        final_metrics = {
            "total_prompt_tokens": usage.get("input_tokens"),
            "total_completion_tokens": usage.get("output_tokens"),
            "total_cached_tokens": usage.get("cache_read_input_tokens"),
            "total_cost_usd": result_msg.total_cost_usd,
            "total_steps": len(steps),
            "extra": {
                "duration_ms": result_msg.duration_ms,
                "num_turns": result_msg.num_turns,
            },
        }

    return {
        "schema_version": "ATIF-v1.2",
        "session_id": result_msg.session_id if result_msg else "unknown",
        "agent": {
            "name": "lightningrod-assistant",
            "version": "2.0.0",
            "tools_used": sorted(tools_used),
        },
        "steps": steps,
        "final_metrics": final_metrics,
    }
