"""KDP Agent Fleet — role-based agents.

Expertise modeled after:
- Jules: plan-then-execute, CI self-heal, async
- Devin: full-task delegation, PR-style output
- OpenHands: sandboxed, model-agnostic
- CircleCI: validation gates, structured failure reports
- Beto: skill/MCP-style reusable patterns
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentResult:
    agent: str
    status: str  # ok | needs_approval | failed
    output: dict[str, Any]
    next_action: str = ""
    logs: list[str] = field(default_factory=list)


def intake_agent(package: dict) -> AgentResult:
    missing = []
    if not package.get("manuscript"):
        missing.append("manuscript")
    if not package.get("cover"):
        missing.append("cover")
    if not package.get("metadata"):
        missing.append("metadata")
    if missing:
        return AgentResult(
            agent="intake",
            status="failed",
            output={"missing": missing},
            next_action="Provide missing files",
            logs=[f"Rejected package. Missing: {missing}"],
        )
    return AgentResult(
        agent="intake",
        status="ok",
        output={"validated": True},
        next_action="Run listing agent",
        logs=["Package validated"],
    )


def listing_agent(metadata: dict) -> AgentResult:
    title = metadata.get("title", "Untitled")
    return AgentResult(
        agent="listing",
        status="ok",
        output={
            "title": title,
            "subtitle": metadata.get("subtitle", ""),
            "description": f"A complete guide to {title}.",
            "keywords": metadata.get("keywords", ["kdp", "book", "publish"]),
            "categories": metadata.get("categories", ["Business"]),
        },
        next_action="Human approval for listing copy",
        logs=["Listing copy generated"],
    )


def orchestrator(package: dict) -> list[AgentResult]:
    results = []
    intake = intake_agent(package)
    results.append(intake)
    if intake.status != "ok":
        return results
    results.append(listing_agent(package.get("metadata", {})))
    return results
