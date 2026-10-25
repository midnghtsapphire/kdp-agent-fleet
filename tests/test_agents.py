"""Test harness for KDP Agent Fleet."""

import pytest
from src.agents import intake_agent, listing_agent, orchestrator, verification_agent


def test_intake_rejects_incomplete():
    result = intake_agent({})
    assert result.status == "failed"
    assert "manuscript" in result.output["missing"]


def test_intake_accepts_complete():
    pkg = {"manuscript": "book.docx", "cover": "cover.jpg", "metadata": {"title": "Test"}}
    result = intake_agent(pkg)
    assert result.status == "ok"


def test_listing_generates_copy():
    result = listing_agent({"title": "KDP Mastery", "keywords": ["kdp", "amazon"]})
    assert result.status == "ok"
    assert "KDP Mastery" in result.output["title"]


def test_verification_passes_clean():
    from src.agents import AgentResult
    clean = [AgentResult("intake", "ok", {})]
    result = verification_agent(clean)
    assert result.status == "ok"


def test_verification_fails_on_errors():
    from src.agents import AgentResult
    bad = [AgentResult("intake", "failed", {})]
    result = verification_agent(bad)
    assert result.status == "failed"


def test_orchestrator_stops_on_failure():
    results = orchestrator({})
    assert len(results) == 1
    assert results[0].status == "failed"


def test_orchestrator_full_happy_path():
    pkg = {
        "manuscript": "book.docx",
        "cover": "cover.jpg",
        "metadata": {"title": "Test Book", "keywords": ["test"]},
    }
    results = orchestrator(pkg)
    assert len(results) == 3  # intake + listing + verification
    assert all(r.status == "ok" for r in results)
