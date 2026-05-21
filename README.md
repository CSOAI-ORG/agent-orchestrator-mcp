[![agent-orchestrator-mcp MCP server](https://glama.ai/mcp/servers/CSOAI-ORG/agent-orchestrator-mcp/badges/score.svg)](https://glama.ai/mcp/servers/CSOAI-ORG/agent-orchestrator-mcp)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-Published-green)](https://registry.modelcontextprotocol.io)
[![PyPI](https://img.shields.io/pypi/v/agent-orchestrator-mcp)](https://pypi.org/project/agent-orchestrator-mcp/)

[![agent-orchestrator-mcp MCP server](https://glama.ai/mcp/servers/CSOAI-ORG/agent-orchestrator-mcp/badges/card.svg)](https://glama.ai/mcp/servers/CSOAI-ORG/agent-orchestrator-mcp)

<div align="center">

> ## 🧱 Part of the MEOK A2A Substrate
>
> This MCP is 1 of 12 agent-to-agent primitives. Run the whole pipeline
> (identity → trust → policy → firewall → rate-limit → handoff → audit
> → governance) as one signed endpoint for **£499/mo** including 100K
> calls — or **£0.0002 per call** pay-as-you-go.
>
> 👉 [meok.ai/a2a](https://meok.ai/a2a) — see the Substrate

# Agent Orchestrator MCP

**MCP server for agent orchestrator mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-agent-orchestrator-mcp)](https://pypi.org/project/meok-agent-orchestrator-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Agent Orchestrator MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `create_agent` | Create a new agent with a name, role, department, and capabilities. |
| `list_agents` | List all registered agents with their trust levels, task counts, and status. |
| `delegate_task` | Delegate a task to a specific agent or auto-route to the best match |
| `complete_task` | Mark a task as completed (or failed). Updates the agent's trust level |
| `acquire_files` | Acquire file locks for coordinated multi-agent work. Prevents conflicts |
| `release_files` | Release file locks held by an agent after task completion. |
| `start_sprint` | Start a focused sprint with named goals and a time limit. Sprints help |
| `complete_sprint` | Complete a sprint and record which goals were achieved. Returns the |
| `get_dashboard` | Get the full orchestration dashboard: agent count, trust averages, |
| `get_task_queue` | Get the task queue, optionally filtered by status (assigned/completed/failed) |

## Installation

```bash
pip install meok-agent-orchestrator-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config:

```json
{
  "mcpServers": {
    "agent-orchestrator-mcp": {
      "command": "python",
      "args": ["-m", "meok_agent_orchestrator_mcp.server"]
    }
  }
}
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
<!-- mcp-name: io.github.CSOAI-ORG/agent-orchestrator-mcp -->

<!-- meok-moat-footer-v1 -->
---

## Pairs with MEOK Governance Suite

Build something that touches users? You need compliance. MEOK ships 38 governance MCPs that drop in alongside this tool — EU AI Act, DORA, NIS2, CRA, GDPR, ISO 42001, FDA SaMD, MDR, Basel, MiFID II, MiCA, COPPA, and more.

```bash
# One-shot install of the governance pack
npx meok-setup --pack governance
```

Free tier: 10 calls/day per MCP. Pro tier (£79/mo): unlimited + cryptographically signed compliance attestations your auditor verifies independently.

→ Full catalogue: [councilof.ai/catalogue](https://councilof.ai/catalogue)
→ MEOK AI Labs: [meok.ai](https://meok.ai)

