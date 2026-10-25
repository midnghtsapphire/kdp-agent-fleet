"""Independent verification layer — Mabl-style copycat.

- Does not grade its own work
- Test impact analysis: maps changes to checks
- Structured failure reports with root cause + fix
- Auto-heal suggestions (does not implement)
- Free local/CI execution
- Designed for MCP/CLI use by coding agents
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class VerificationResult:
    status: str  # pass | fail | needs_coverage
    impacted_checks: list[str]
    failures: list[dict[str, Any]] = field(default_factory=list)
    coverage_gaps: list[str] = field(default_factory=list)
    auto_heal_suggestions: list[str] = field(default_factory=list)
    logs: list[str] = field(default_factory=list)


def impact_analysis(change_description: str, known_checks: list[str]) -> list[str]:
    """Simple TIA: return checks likely affected by the change."""
    keywords = change_description.lower().split()
    impacted = []
    for check in known_checks:
        if any(k in check.lower() for k in keywords) or any(k in change_description.lower() for k in check.lower().split()):
            impacted.append(check)
    return impacted or known_checks[:1]  # fallback to at least one


def verify_package(package: dict, change_description: str = "") -> VerificationResult:
    """Independent verification. Caller must not be the agent that produced the package."""
    known_checks = [
        "manuscript present",
        "cover present",
        "metadata complete",
        "title length",
        "keyword count",
    ]
    impacted = impact_analysis(change_description or "full package", known_checks)

    failures = []
    if not package.get("manuscript"):
        failures.append({"check": "manuscript present", "root_cause": "missing file", "fix": "provide .docx or .epub"})
    if not package.get("cover"):
        failures.append({"check": "cover present", "root_cause": "missing file", "fix": "provide cover image meeting KDP size/DPI"})
    meta = package.get("metadata", {})
    if not meta.get("title"):
        failures.append({"check": "metadata complete", "root_cause": "title missing", "fix": "add title"})
    if meta.get("keywords") and len(meta.get("keywords", [])) > 7:
        failures.append({"check": "keyword count", "root_cause": "too many keywords", "fix": "limit to 7"})

    gaps = [c for c in known_checks if c not in impacted]
    suggestions = []
    if failures:
        suggestions.append("Auto-heal: regenerate listing metadata from manuscript if available")

    status = "fail" if failures else "pass"

    return VerificationResult(
        status=status,
        impacted_checks=impacted,
        failures=failures,
        coverage_gaps=gaps,
        auto_heal_suggestions=suggestions,
        logs=[f"Independent verification complete. Status: {status}"],
    )
