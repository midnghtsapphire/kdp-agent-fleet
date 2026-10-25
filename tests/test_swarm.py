"""Tests for OpenRouter swarm."""

from src.swarm import swarm_verify


def test_swarm_fails_incomplete():
    result = swarm_verify({})
    assert result.status == "fail"


def test_swarm_passes_complete():
    pkg = {
        "manuscript": "book.docx",
        "cover": "cover.jpg",
        "metadata": {"title": "Test", "keywords": ["a"]},
    }
    result = swarm_verify(pkg)
    assert result.status == "pass"
    assert len(result.agent_results) >= 2
