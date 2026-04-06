"""
Harbor agent adapter for the lightningrod-assistant Claude Code agent.

Runs the claude CLI on the HOST (not inside Docker) since it uses OAuth
credentials from the local credential store. Writes the response into
the Docker container for the verifier to score.
"""

import json
import subprocess
from pathlib import Path

from harbor.agents.base import BaseAgent
from harbor.environments.base import BaseEnvironment
from harbor.models.agent.context import AgentContext

# Repo root on the host — agent needs this as cwd for .claude/ directory access
SDK_ROOT = Path(__file__).resolve().parent.parent


class LightningrodAssistantAgent(BaseAgent):
    """Wraps the lightningrod-assistant Claude Code agent for Harbor evaluation."""

    AGENT_NAME = "lightningrod-assistant"
    TIMEOUT_SEC = 240

    @staticmethod
    def name() -> str:
        return "lightningrod-assistant"

    def version(self) -> str | None:
        return "1.0.0"

    async def setup(self, environment: BaseEnvironment) -> None:
        pass

    async def run(
        self,
        instruction: str,
        environment: BaseEnvironment,
        context: AgentContext,
    ) -> None:
        # Run claude CLI on the host — it uses local OAuth credentials
        cmd = [
            "claude",
            "-p",  # print mode (non-interactive)
            "--agent", self.AGENT_NAME,
            "--output-format", "json",
            "--dangerously-skip-permissions",
            "--max-turns", "10",
            instruction,
        ]

        self.logger.info(f"Running claude CLI on host with cwd={SDK_ROOT}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.TIMEOUT_SEC,
                cwd=str(SDK_ROOT),
            )
        except subprocess.TimeoutExpired:
            response_text = "[AGENT ERROR] Claude CLI timed out"
            await self._write_response(environment, response_text)
            context.metadata = {"error": "timeout"}
            return

        # Parse the response
        response_text = self._parse_response(result.stdout, result.stderr)

        # Write response into the Docker container for the verifier
        await self._write_response(environment, response_text)

        context.metadata = {
            "response_length": len(response_text),
            "return_code": result.returncode,
            "stderr_preview": (result.stderr or "")[:500],
        }

    def _parse_response(self, stdout: str, stderr: str) -> str:
        """Parse claude CLI JSON output into plain text response."""
        if not stdout.strip():
            return f"[AGENT ERROR] No output\n{stderr}" if stderr else "[AGENT ERROR] No output"

        try:
            output = json.loads(stdout)
            if isinstance(output, dict):
                return output.get("result", stdout)
            elif isinstance(output, list):
                return "\n".join(
                    msg.get("content", str(msg))
                    for msg in output
                    if isinstance(msg, dict)
                )
            return stdout
        except (json.JSONDecodeError, KeyError):
            return stdout

    async def _write_response(
        self, environment: BaseEnvironment, response_text: str
    ) -> None:
        """Write the agent response into the container for the verifier."""
        await environment.exec("mkdir -p /logs/agent", timeout_sec=10)

        # Use base64 to safely transfer arbitrary text into the container
        import base64
        encoded = base64.b64encode(response_text.encode()).decode()
        await environment.exec(
            f"echo '{encoded}' | base64 -d > /logs/agent/response.txt",
            timeout_sec=10,
        )
