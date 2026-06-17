---
icon: robot
description: Use Lightning Rod from AI agents and Claude Code via the plugin, assistant agent, and skills.
---

# Using Lightning Rod with AI Agents

The Lightning Rod SDK ships with a Claude Code plugin that teaches AI agents how to build forecasting datasets and fine-tune models using proven patterns.

### Claude Code

The easiest way to use Lightning Rod skills in a separate project is via the Claude Code plugin system:

```
/plugin marketplace add lightning-rod-labs/lightningrod-python-sdk
/plugin install lightningrod-python-sdk
```

This installs all skills and the `lightningrod-assistant` agent into your project. Skills are namespaced under the `lightningrod-python-sdk` plugin.

Try it with a fine-tuning prompt:

```bash
claude "Build a forecasting model to predict PGA Tour players will finish in the top 20"
```

### Other agents

Any MCP-compatible client (Hermes, OpenClaw, Codex, etc.) can connect by adding the streamable HTTP endpoint above as an MCP server in its configuration. The server exposes a `search-docs` tool that agents use to look up SDK concepts, parameters, and usage patterns.
