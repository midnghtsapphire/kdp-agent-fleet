"""OpenRouter swarm — Cubic-style parallel agents.

Runs multiple specialized agents in parallel against a package or change,
then aggregates findings. Uses OpenRouter for model routing.

Login rule: first call must use a paid model. Free models allowed after.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any
import os
import json
from pathlib import Path

from .agents import AgentResult, intake_agent, listing_agent, verification_agent
from .verification import verify_package

PAID_MODELS = {
    "openai/gpt-4o-mini",
    "openai/gpt-4o",
    "anthropic/claude-3.5-sonnet",
    "anthropic/claude-3-haiku",
    "google/gemini-pro",
}
FREE_MODELS = {
    "meta-llama/llama-3.1-8b-instruct:free",
    "google/gemma-2-9b-it:free",
    "mistralai/mistral-7b-instruct:free",
}
STATE_FILE = Path.home() / ".kdp-fleet-state.json"


def _load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"paid_login_done": False}


def _save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state))


def require_paid_on_login(model: str) -> None:
    """First call must be a paid model. Free allowed after."""
    state = _load_state()
    if not state.get("paid_login_done"):
        if model not in PAID_MODELS and ":free" in model:
            raise ValueError(
                f"First login requires a paid model. Got free model '{model}'. "
                f"Use one of: {sorted(PAID_MODELS)}"
            )
        state["paid_login_done"] = True
        _save_state(state)


@dataclass
class SwarmResult:
    status: str
    agent_results: list[AgentResult]
    findings: list[dict[str, Any]] = field(default_factory=list)
    logs: list[str] = field(default_factory=list)


def _run_agent(name: str, fn, arg) -> AgentResult:
    try:
        return fn(arg)
    except Exception as e:
        return AgentResult(
            agent=name,
            status="failed",
            output={"error": str(e)},
            next_action="Retry or escalate",
            logs=[f"{name} failed: {e}"],
        )


def swarm_verify(package: dict, change_description: str = "", max_workers: int = 4) -> SwarmResult:
    """Run multiple agents in parallel, then independent verification."""
    tasks = [
        ("intake", intake_agent, package),
        ("listing", listing_agent, package.get("metadata", {})),
        ("verification", verification_agent, []),
    ]

    results: list[AgentResult] = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(_run_agent, name, fn, arg): name for name, fn, arg in tasks}
        for fut in as_completed(futures):
            results.append(fut.result())

    v = verify_package(package, change_description)
    findings = [{"source": "verification", "status": v.status, "failures": v.failures}]

    status = "pass" if all(r.status == "ok" for r in results) and v.status == "pass" else "fail"
    return SwarmResult(
        status=status,
        agent_results=results,
        findings=findings,
        logs=["Swarm complete"],
    )


def openrouter_call(prompt: str, model: str = "openai/gpt-4o-mini") -> str:
    """OpenRouter call. First use must be a paid model."""
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        return "OPENROUTER_API_KEY not set — dry run"
    require_paid_on_login(model)
    # Real call would go here
    return f"[OpenRouter {model}] {prompt[:80]}..."
