> **By [MEOK AI Labs](https://meok.ai)** — Sovereign AI tools for everyone.

# Agent Orchestrator MCP Server

Multi-agent task management system for AI applications. Create agents with roles and capabilities, delegate tasks with trust-based routing, coordinate file access to prevent conflicts, run focused sprints, and monitor performance through a unified dashboard.

Based on the Sovereign Temple 47-agent coordination framework, simplified for standalone use. Data persists in `~/.mcp-agents/`.

## Tools

| Tool | Description |
|------|-------------|
| `create_agent` | Register an agent with name, role, department, and capabilities |
| `list_agents` | List all agents with trust levels and task counts |
| `delegate_task` | Assign tasks to specific agents or auto-route by capability/trust |
| `complete_task` | Mark tasks done, update agent trust based on success/failure |
| `acquire_files` | Lock files for coordinated multi-agent editing |
| `release_files` | Release file locks after task completion |
| `start_sprint` | Begin a focused sprint with goals and time limit |
| `complete_sprint` | Close a sprint and record completion rate |
| `get_dashboard` | Full orchestration overview: agents, tasks, sprints, locks |
| `get_task_queue` | Browse tasks filtered by status or agent |

## Installation

```bash
pip install mcp
```

## Usage

### Run the server

```bash
python server.py
```

### Claude Desktop config

```json
{
  "mcpServers": {
    "agent-orchestrator": {
      "command": "python",
      "args": ["/path/to/agent-orchestrator-mcp/server.py"]
    }
  }
}
```

### Example workflow

**1. Create agents:**
```
Tool: create_agent
Input: {"name": "Research Bot", "role": "researcher", "department": "research", "capabilities": ["web_search", "analysis"]}
Output: {"status": "created", "agent_id": "research_bot", "role": "researcher"}
```

**2. Delegate a task:**
```
Tool: delegate_task
Input: {"task": "Research competitor pricing models", "capability": "web_search", "priority": "high"}
Output: {"status": "delegated", "task_id": "a1b2c3d4", "agent_id": "research_bot"}
```

**3. Coordinate file access:**
```
Tool: acquire_files
Input: {"agent_id": "research_bot", "files": ["report.md", "data.json"], "task_id": "a1b2c3d4", "exclusive": true}
Output: {"status": "acquired", "files": ["report.md", "data.json"]}
```

**4. Complete the task:**
```
Tool: complete_task
Input: {"task_id": "a1b2c3d4", "agent_id": "research_bot", "result_summary": "Found 5 competitor pricing tiers...", "care_score": 0.8}
Output: {"status": "completed", "task_id": "a1b2c3d4"}
```

**5. Check the dashboard:**
```
Tool: get_dashboard
Output: {"agents": {"total": 3, "active": 3, "avg_trust": 0.52}, "tasks": {"total": 12, "by_status": {"completed": 8, "assigned": 4}}, ...}
```

## Trust System

Agents accumulate trust through successful task completion:
- Successful task: trust += 0.02 x care_score (max 1.0)
- Failed task: trust -= 0.05 (min 0.0)
- Auto-routing prefers higher-trust agents
- Trust persists across sessions

## Data Storage

All data persists in `~/.mcp-agents/`:
- `agents.json` - Agent registry
- `tasks.json` - Task history
- `sprints.json` - Sprint records

## Pricing

| Tier | Limit | Price |
|------|-------|-------|
| Free | 100 calls/day, 10 agents max | $0 |
| Pro | Unlimited agents, webhook notifications, LLM-powered routing | $9/mo |
| Enterprise | Custom + team sharing + audit logs + SSO | Contact us |

## License

MIT
