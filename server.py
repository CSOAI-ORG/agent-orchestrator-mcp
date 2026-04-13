#!/usr/bin/env python3
"""
Agent Orchestrator MCP Server
===============================
Multi-agent task management system. Create agents with roles and capabilities,
delegate tasks with trust-based routing, coordinate multi-agent file access,
run sprint workflows, and monitor agent performance. Based on the Sovereign
Temple 47-agent coordination framework.

Install: pip install mcp
Run:     python server.py
"""

import json
import uuid
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------
FREE_DAILY_LIMIT = 100
FREE_MAX_AGENTS = 10
_usage: dict[str, list[datetime]] = defaultdict(list)


def _check_rate_limit(caller: str = "anonymous") -> Optional[str]:
    now = datetime.now()
    cutoff = now - timedelta(days=1)
    _usage[caller] = [t for t in _usage[caller] if t > cutoff]
    if len(_usage[caller]) >= FREE_DAILY_LIMIT:
        return f"Free tier limit reached ({FREE_DAILY_LIMIT}/day). Upgrade to Pro: https://mcpize.com/agent-orchestrator-mcp/pro"
    _usage[caller].append(now)
    return None


# ---------------------------------------------------------------------------
# Persistent Storage
# ---------------------------------------------------------------------------
DATA_DIR = Path.home() / ".mcp-agents"
DATA_DIR.mkdir(exist_ok=True)
AGENTS_FILE = DATA_DIR / "agents.json"
TASKS_FILE = DATA_DIR / "tasks.json"
SPRINTS_FILE = DATA_DIR / "sprints.json"


def _load_json(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def _save_json(path: Path, data: dict):
    path.write_text(json.dumps(data, indent=2, default=str))


# ---------------------------------------------------------------------------
# Agent Registry
# ---------------------------------------------------------------------------
class AgentStore:
    def __init__(self):
        self.agents = _load_json(AGENTS_FILE)
        self.tasks = _load_json(TASKS_FILE)
        self.sprints = _load_json(SPRINTS_FILE)
        self._file_locks: dict[str, dict] = {}  # file -> {"agent": str, "task": str, "exclusive": bool}

    def save(self):
        _save_json(AGENTS_FILE, self.agents)
        _save_json(TASKS_FILE, self.tasks)
        _save_json(SPRINTS_FILE, self.sprints)

    def create_agent(self, name: str, role: str, department: str = "general",
                     capabilities: list[str] | None = None,
                     instructions: str = "") -> dict:
        aid = name.lower().replace(" ", "_")
        if aid in self.agents and len(self.agents) >= FREE_MAX_AGENTS:
            pass  # Allow update
        elif len(self.agents) >= FREE_MAX_AGENTS and aid not in self.agents:
            return {"error": f"Free tier limit: max {FREE_MAX_AGENTS} agents. Upgrade for unlimited."}

        now = datetime.now().isoformat()
        self.agents[aid] = {
            "name": name,
            "role": role,
            "department": department,
            "capabilities": capabilities or [],
            "instructions": instructions,
            "trust_level": 0.5,
            "tasks_completed": self.agents.get(aid, {}).get("tasks_completed", 0),
            "tasks_failed": self.agents.get(aid, {}).get("tasks_failed", 0),
            "created_at": self.agents.get(aid, {}).get("created_at", now),
            "updated_at": now,
            "status": "active",
        }
        self.save()
        return {"status": "created", "agent_id": aid, "name": name, "role": role}

    def get_agent(self, aid: str) -> Optional[dict]:
        return self.agents.get(aid)

    def list_agents(self, department: str | None = None) -> list[dict]:
        agents = []
        for aid, agent in self.agents.items():
            if department and agent.get("department") != department:
                continue
            agents.append({"id": aid, **agent})
        return agents

    def find_best_agent(self, capability: str | None = None,
                        department: str | None = None) -> Optional[str]:
        """Find the best agent for a task based on capability match and trust level."""
        candidates = []
        for aid, agent in self.agents.items():
            if agent.get("status") != "active":
                continue
            if department and agent.get("department") != department:
                continue
            if capability and capability not in agent.get("capabilities", []):
                continue
            candidates.append((aid, agent.get("trust_level", 0.5)))

        if not candidates:
            return None
        # Sort by trust level descending
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0][0]

    def delegate_task(self, task_desc: str, agent_id: str | None = None,
                      capability: str | None = None,
                      department: str | None = None,
                      priority: str = "normal",
                      care_score: float = 0.5) -> dict:
        """Delegate a task to a specific agent or auto-route to best match."""
        if not agent_id:
            agent_id = self.find_best_agent(capability, department)
        if not agent_id or agent_id not in self.agents:
            return {"error": f"Agent '{agent_id}' not found. Create an agent first."}

        tid = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        task = {
            "id": tid,
            "description": task_desc,
            "agent_id": agent_id,
            "agent_name": self.agents[agent_id]["name"],
            "status": "assigned",
            "priority": priority,
            "care_score": care_score,
            "created_at": now,
            "updated_at": now,
            "result": None,
        }
        self.tasks[tid] = task
        self.save()
        return {"status": "delegated", "task_id": tid, "agent_id": agent_id,
                "agent_name": self.agents[agent_id]["name"], "task": task_desc}

    def complete_task(self, task_id: str, agent_id: str,
                      result_summary: str, care_score: float = 0.5,
                      success: bool = True) -> dict:
        """Mark a task as completed and update agent trust."""
        if task_id not in self.tasks:
            return {"error": f"Task {task_id} not found"}

        task = self.tasks[task_id]
        task["status"] = "completed" if success else "failed"
        task["result"] = result_summary
        task["care_score"] = care_score
        task["updated_at"] = datetime.now().isoformat()

        # Update agent trust based on outcome
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            if success:
                agent["tasks_completed"] = agent.get("tasks_completed", 0) + 1
                # Trust increases with successful completions
                trust_delta = 0.02 * care_score
                agent["trust_level"] = min(1.0, agent.get("trust_level", 0.5) + trust_delta)
            else:
                agent["tasks_failed"] = agent.get("tasks_failed", 0) + 1
                trust_delta = -0.05
                agent["trust_level"] = max(0.0, agent.get("trust_level", 0.5) + trust_delta)

        self.save()
        return {"status": task["status"], "task_id": task_id, "agent_id": agent_id,
                "result": result_summary}

    def acquire_files(self, agent_id: str, files: list[str], task_id: str,
                      exclusive: bool = False) -> dict:
        """Acquire file locks for coordinated multi-agent work."""
        conflicts = []
        for f in files:
            if f in self._file_locks:
                lock = self._file_locks[f]
                if lock["exclusive"] or exclusive:
                    conflicts.append({"file": f, "locked_by": lock["agent"]})

        if conflicts:
            return {"status": "conflict", "conflicts": conflicts}

        for f in files:
            self._file_locks[f] = {
                "agent": agent_id,
                "task": task_id,
                "exclusive": exclusive,
                "acquired_at": datetime.now().isoformat(),
            }
        return {"status": "acquired", "files": files, "agent_id": agent_id}

    def release_files(self, agent_id: str, files: list[str]) -> dict:
        """Release file locks."""
        released = []
        for f in files:
            if f in self._file_locks and self._file_locks[f]["agent"] == agent_id:
                del self._file_locks[f]
                released.append(f)
        return {"status": "released", "files": released}

    def start_sprint(self, name: str, goals: list[str], duration_minutes: int = 60) -> dict:
        """Start a focused sprint with goals and time limit."""
        sid = str(uuid.uuid4())[:8]
        now = datetime.now()
        sprint = {
            "id": sid,
            "name": name,
            "goals": goals,
            "status": "active",
            "started_at": now.isoformat(),
            "ends_at": (now + timedelta(minutes=duration_minutes)).isoformat(),
            "duration_minutes": duration_minutes,
            "completed_goals": [],
            "tasks": [],
        }
        self.sprints[sid] = sprint
        self.save()
        return {"status": "started", "sprint_id": sid, "name": name,
                "ends_at": sprint["ends_at"], "goals": goals}

    def complete_sprint(self, sprint_id: str, completed_goals: list[str] | None = None,
                        summary: str = "") -> dict:
        """Complete a sprint and record results."""
        if sprint_id not in self.sprints:
            return {"error": f"Sprint {sprint_id} not found"}

        sprint = self.sprints[sprint_id]
        sprint["status"] = "completed"
        sprint["completed_at"] = datetime.now().isoformat()
        sprint["completed_goals"] = completed_goals or []
        sprint["summary"] = summary

        total = len(sprint["goals"])
        done = len(sprint["completed_goals"])
        sprint["completion_rate"] = round(done / max(total, 1) * 100, 1)

        self.save()
        return {
            "status": "completed",
            "sprint_id": sprint_id,
            "completion_rate": sprint["completion_rate"],
            "completed": done,
            "total": total,
            "summary": summary,
        }

    def get_dashboard(self) -> dict:
        """Get full orchestration dashboard."""
        total_agents = len(self.agents)
        active_agents = sum(1 for a in self.agents.values() if a.get("status") == "active")

        total_tasks = len(self.tasks)
        by_status = defaultdict(int)
        for t in self.tasks.values():
            by_status[t.get("status", "unknown")] += 1

        avg_trust = 0
        if self.agents:
            avg_trust = sum(a.get("trust_level", 0.5) for a in self.agents.values()) / len(self.agents)

        active_sprints = [s for s in self.sprints.values() if s.get("status") == "active"]
        file_locks = len(self._file_locks)

        # Department breakdown
        departments = defaultdict(int)
        for a in self.agents.values():
            departments[a.get("department", "general")] += 1

        return {
            "agents": {"total": total_agents, "active": active_agents, "avg_trust": round(avg_trust, 3)},
            "tasks": {"total": total_tasks, "by_status": dict(by_status)},
            "sprints": {"active": len(active_sprints), "total": len(self.sprints)},
            "file_locks": file_locks,
            "departments": dict(departments),
        }


# Global store
store = AgentStore()

# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "Agent Orchestrator MCP",
    instructions="Multi-agent task management: create agents, delegate tasks with trust-based routing, coordinate file access, run sprints, and monitor performance.",
)


@mcp.tool()
def create_agent(name: str, role: str, department: str = "general",
                 capabilities: list[str] | None = None,
                 instructions: str = "") -> dict:
    """Create a new agent with a name, role, department, and capabilities.
    Agents accumulate trust through successful task completion.
    Free tier: max 10 agents."""
    err = _check_rate_limit()
    if err:
        return {"error": err}
    return store.create_agent(name, role, department, capabilities, instructions)


@mcp.tool()
def list_agents(department: str | None = None) -> dict:
    """List all registered agents with their trust levels, task counts, and status.
    Optionally filter by department."""
    err = _check_rate_limit()
    if err:
        return {"error": err}
    agents = store.list_agents(department)
    return {"agents": agents, "count": len(agents)}


@mcp.tool()
def delegate_task(task: str, agent_id: str | None = None,
                  capability: str | None = None,
                  department: str | None = None,
                  priority: str = "normal",
                  care_score: float = 0.5) -> dict:
    """Delegate a task to a specific agent or auto-route to the best match
    based on capability, department, and trust level. Priority: low/normal/high/urgent.
    Care score (0-1) influences trust updates on completion."""
    err = _check_rate_limit()
    if err:
        return {"error": err}
    return store.delegate_task(task, agent_id, capability, department, priority, care_score)


@mcp.tool()
def complete_task(task_id: str, agent_id: str, result_summary: str,
                  care_score: float = 0.5, success: bool = True) -> dict:
    """Mark a task as completed (or failed). Updates the agent's trust level
    based on success/failure and care score. Successful tasks increase trust,
    failed tasks decrease it."""
    err = _check_rate_limit()
    if err:
        return {"error": err}
    return store.complete_task(task_id, agent_id, result_summary, care_score, success)


@mcp.tool()
def acquire_files(agent_id: str, files: list[str], task_id: str,
                  exclusive: bool = False) -> dict:
    """Acquire file locks for coordinated multi-agent work. Prevents conflicts
    when multiple agents need to modify the same files. Set exclusive=true for
    write locks, false for read locks."""
    err = _check_rate_limit()
    if err:
        return {"error": err}
    return store.acquire_files(agent_id, files, task_id, exclusive)


@mcp.tool()
def release_files(agent_id: str, files: list[str]) -> dict:
    """Release file locks held by an agent after task completion."""
    err = _check_rate_limit()
    if err:
        return {"error": err}
    return store.release_files(agent_id, files)


@mcp.tool()
def start_sprint(name: str, goals: list[str], duration_minutes: int = 60) -> dict:
    """Start a focused sprint with named goals and a time limit. Sprints help
    agents coordinate on a set of objectives within a deadline."""
    err = _check_rate_limit()
    if err:
        return {"error": err}
    return store.start_sprint(name, goals, duration_minutes)


@mcp.tool()
def complete_sprint(sprint_id: str, completed_goals: list[str] | None = None,
                    summary: str = "") -> dict:
    """Complete a sprint and record which goals were achieved. Returns the
    completion rate percentage."""
    err = _check_rate_limit()
    if err:
        return {"error": err}
    return store.complete_sprint(sprint_id, completed_goals, summary)


@mcp.tool()
def get_dashboard() -> dict:
    """Get the full orchestration dashboard: agent count, trust averages,
    task breakdown by status, active sprints, file locks, and department distribution."""
    err = _check_rate_limit()
    if err:
        return {"error": err}
    return store.get_dashboard()


@mcp.tool()
def get_task_queue(status: str | None = None, agent_id: str | None = None,
                   limit: int = 20) -> dict:
    """Get the task queue, optionally filtered by status (assigned/completed/failed)
    or agent. Returns tasks sorted by most recent."""
    err = _check_rate_limit()
    if err:
        return {"error": err}

    tasks = []
    for tid, task in sorted(store.tasks.items(),
                             key=lambda x: x[1].get("updated_at", ""), reverse=True):
        if status and task.get("status") != status:
            continue
        if agent_id and task.get("agent_id") != agent_id:
            continue
        tasks.append(task)
        if len(tasks) >= limit:
            break

    return {"tasks": tasks, "count": len(tasks)}


if __name__ == "__main__":
    mcp.run()
