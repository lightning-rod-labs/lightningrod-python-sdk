#!/usr/bin/env python3
"""Extract a Claude Code session transcript as readable markdown.

Usage:
    python scripts/extract_session.py                     # list recent sessions
    python scripts/extract_session.py <session-id>        # full transcript
    python scripts/extract_session.py <session-id> --last 10  # last 10 exchanges
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Claude Code stores sessions relative to the project path
PROJECT_KEY = "-Users-bart-Projects-lightningrod-python-sdk"
SESSIONS_DIR = Path.home() / ".claude" / "projects" / PROJECT_KEY


def list_sessions(n: int = 10) -> None:
    """List the most recent sessions with a preview of the first user message."""
    jsonl_files = sorted(
        SESSIONS_DIR.glob("*.jsonl"),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    if not jsonl_files:
        print("No sessions found.", file=sys.stderr)
        sys.exit(1)

    print(f"Recent sessions (newest first):\n")
    for f in jsonl_files[:n]:
        session_id = f.stem
        preview = _first_user_message(f)
        agent = _agent_setting(f)
        agent_tag = f"  [{agent}]" if agent else ""
        print(f"  {session_id}{agent_tag}")
        if preview:
            print(f"    {preview[:120]}")
        print()


def _agent_setting(path: Path) -> str | None:
    """Extract the agent name from the session file."""
    with open(path) as fh:
        for line in fh:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("type") == "agent-setting":
                return record.get("agentSetting")
    return None


def _first_user_message(path: Path) -> str | None:
    """Extract the first user message text from a session file."""
    with open(path) as fh:
        for line in fh:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("type") != "user":
                continue
            msg = record.get("message", {})
            if not isinstance(msg, dict) or msg.get("role") != "user":
                continue
            text = _extract_text(msg.get("content", ""))
            if text and not _is_command_wrapper(text):
                return text
    return None


def _extract_text(content) -> str:
    """Extract plain text from message content (string or content blocks)."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text = block.get("text", "").strip()
                if text:
                    parts.append(text)
        return "\n".join(parts)
    return ""


def _is_command_wrapper(text: str) -> bool:
    """Check if a user message is a local command wrapper (not real user input)."""
    return text.startswith("<local-command") or text.startswith("<command-name>")


def extract_transcript(session_id: str, last_n: int | None = None) -> str:
    """Extract a markdown transcript from a session JSONL file."""
    path = SESSIONS_DIR / f"{session_id}.jsonl"
    if not path.exists():
        print(f"Session not found: {session_id}", file=sys.stderr)
        print(f"Looked in: {SESSIONS_DIR}", file=sys.stderr)
        print(f"\nTry listing sessions: python {__file__}", file=sys.stderr)
        sys.exit(1)

    exchanges = []
    with open(path) as fh:
        for line in fh:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            msg = record.get("message", {})
            if not isinstance(msg, dict):
                continue
            role = msg.get("role")
            if role not in ("user", "assistant"):
                continue

            content = msg.get("content", "")

            if role == "user":
                text = _extract_text(content)
                if not text or _is_command_wrapper(text):
                    continue
                exchanges.append(("user", text))

            elif role == "assistant":
                parts = []
                if isinstance(content, list):
                    for block in content:
                        if not isinstance(block, dict):
                            continue
                        if block.get("type") == "text":
                            text = block.get("text", "").strip()
                            if text:
                                parts.append(text)
                        elif block.get("type") == "tool_use":
                            tool_name = block.get("name", "unknown")
                            parts.append(f"[Tool: {tool_name}]")
                elif isinstance(content, str) and content.strip():
                    parts.append(content.strip())

                if parts:
                    exchanges.append(("assistant", "\n".join(parts)))

    if last_n is not None:
        exchanges = exchanges[-last_n:]

    # Format as markdown
    output = []
    for role, text in exchanges:
        header = "## User" if role == "user" else "## Assistant"
        output.append(f"{header}\n\n{text}\n")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Extract a Claude Code session transcript."
    )
    parser.add_argument(
        "session_id",
        nargs="?",
        help="Session UUID. Omit to list recent sessions.",
    )
    parser.add_argument(
        "--last",
        type=int,
        default=None,
        help="Only include the last N exchanges.",
    )
    args = parser.parse_args()

    if args.session_id is None:
        list_sessions()
    else:
        transcript = extract_transcript(args.session_id, last_n=args.last)
        print(transcript)


if __name__ == "__main__":
    main()
