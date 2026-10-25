"""OpenRouter swarm — Cubic-style parallel agents.

Runs multiple specialized agents in parallel against a package or change,
then aggregates findings. Uses OpenRouter for model routing.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any
import os

from .agents import AgentResult, intake_agent, listing_agent, verification_agent
from .verification import verify_package


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

    # Independent verification pass
    v = verify_package(package, change_description)
    findings = [{"source": "verification", "status": v.status, "failures": v.failures}]

    status = "pass" if all(r.status == "ok" for r in results) and v.status == "pass" else "fail"
    return SwarmResult(
        status=status,
        agent_results=results,
        findings=findings,
        logs=["Swarm complete via OpenRouter routing (placeholder for model calls)"],
    )


def openrouter_call(prompt: str, model: str = "openai/gpt-4o-mini") -> str:
    """Placeholder for OpenRouter. Set OPENROUTER_API_KEY to enable."""
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        return "OPENROUTER_API_KEY not set — dry run"
    # Real call would go here
    return f"[OpenRouter {model}] {prompt[:80]}..."
