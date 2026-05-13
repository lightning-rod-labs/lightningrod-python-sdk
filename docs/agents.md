---
icon: robot
---

# Using Lightning Rod with AI Agents

The Lightning Rod SDK ships with **skills** — structured knowledge files that teach AI agents how to build forecasting datasets and fine-tune models using proven patterns. Skills live in the top-level `skills/` directory and work across multiple agent frameworks.

## Available Skills

| Skill | What it teaches |
|-------|----------------|
| `lightningrod-assistant` | End-to-end orchestration skill — flow, communication style, answer-type selection, hard constraints. Mirrors the Claude Code `lightningrod-assistant` agent so non-Claude-Code agents (Hermes, OpenClaw, Codex) get a similar behavior. |
| `examples-guide` | Decision tree: forward-looking (GRPO) vs content learning (SFT) vs tabular. Starting point for new projects. |
| `forward-looking-examples` | Production GRPO configs: golf, Trump policy, military strikes, Foresight/GDELT, FileSet RAG. |
| `content-learning-examples` | SFT patterns: TopicTree + WebSearch, FileSet + QuestionAndLabel. |
| `tabular-examples` | Structured data → Sample mapping: `create_sample()`, `TemplateQuestionGenerator`, supply chain detection. |
| `bigquery-seeds` | BigQuery seed sourcing. No GCP credentials needed — Lightning Rod manages access. |
| `custom-dataset-seeds` | File/CSV/PDF → seeds via preprocessing, FileSet uploads, and `CsvSeedGenerator`. |
| `public-dataset-exploration` | Finding datasets on Kaggle, HuggingFace, GitHub when you have a domain but no data. |
| `transform-pipeline-verification` | Post-run inspection: download samples, spot-check quality, iterate before scaling. |

## Agent Setup

### Claude Code

The easiest way to use Lightning Rod skills in a separate project is via the Claude Code plugin system:

```
/plugin marketplace add lightning-rod-labs/lightningrod-python-sdk
/plugin install lightningrod-python-sdk
```

This installs all skills and the `lightningrod-assistant` agent into your project. Skills are namespaced under the `lightningrod-python-sdk` plugin.

## Documentation MCP Server

Lightning Rod hosts a Model Context Protocol server that exposes the official SDK docs to your agent. Once connected, agents can search the docs on demand instead of guessing at API signatures.

**Server URL:** `https://docs.lightningrod.ai/~gitbook/mcp` (streamable HTTP, no auth required)

### Claude Code

Add it to your `~/.claude.json` (or project-level `.mcp.json`):

```json
{
  "mcpServers": {
    "lightningrod-docs": {
      "type": "http",
      "url": "https://docs.lightningrod.ai/~gitbook/mcp"
    }
  }
}
```

The `lightningrod-assistant` agent shipped via the plugin already wires this in — you only need the config above if you're using the SDK without the plugin.

### Other agents

Any MCP-compatible client (Hermes, OpenClaw, Codex, etc.) can connect by adding the streamable HTTP endpoint above as an MCP server in its configuration. The server exposes a `search-docs` tool that agents use to look up SDK concepts, parameters, and usage patterns.
