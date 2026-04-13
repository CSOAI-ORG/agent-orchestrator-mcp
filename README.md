# Agent Orchestrator MCP Server

> **By [MEOK AI Labs](https://meok.ai)** — Sovereign AI tools for everyone.

Multi-agent task management system for AI applications. Create agents with roles and capabilities, delegate tasks with trust-based routing, coordinate file access, run focused sprints, and monitor performance through a unified dashboard.

[![MCPize](https://img.shields.io/badge/MCPize-Listed-blue)](https://mcpize.com/mcp/agent-orchestrator)
[![MIT License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-255+_servers-purple)](https://meok.ai)

## Tools

| Tool | Description |
|------|-------------|
| `create_agent` | Create a new agent with name, role, and capabilities |
| `list_agents` | List all registered agents with trust levels and status |
| `delegate_task` | Delegate a task to an agent or auto-route to best match |
| `complete_task` | Mark a task as completed or failed |
| `acquire_files` | Acquire file locks for coordinated multi-agent work |
| `release_files` | Release file locks held by an agent |
| `start_sprint` | Start a focused sprint with goals and a time limit |
| `complete_sprint` | Complete a sprint and record achieved goals |
| `get_dashboard` | Get the full orchestration dashboard |
| `get_task_queue` | Get the task queue filtered by status |

## Quick Start

```bash
pip install mcp
git clone https://github.com/CSOAI-ORG/agent-orchestrator-mcp.git
cd agent-orchestrator-mcp
python server.py
```

## Claude Desktop Config

```json
{
  "mcpServers": {
    "agent-orchestrator": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/path/to/agent-orchestrator-mcp"
    }
  }
}
```

## Pricing

| Plan | Price | Requests |
|------|-------|----------|
| Free | $0/mo | 100 calls/day, 10 agents max |
| Pro | $9/mo | Unlimited agents + webhook notifications |
| Enterprise | Contact us | Custom + LLM-powered routing |

[Get on MCPize](https://mcpize.com/mcp/agent-orchestrator)

## Part of MEOK AI Labs

This is one of 255+ MCP servers by MEOK AI Labs. Browse all at [meok.ai](https://meok.ai) or [GitHub](https://github.com/CSOAI-ORG).

---
**MEOK AI Labs** | [meok.ai](https://meok.ai) | nicholas@meok.ai | United Kingdom
