"""Tests for OpenRouter swarm and paid-on-login rule."""

import pytest
from src.swarm import swarm_verify, require_paid_on_login, PAID_MODELS


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


def test_first_login_rejects_free():
    with pytest.raises(ValueError, match="paid model"):
        require_paid_on_login("meta-llama/llama-3.1-8b-instruct:free")


def test_first_login_accepts_paid():
    require_paid_on_login("openai/gpt-4o-mini")  # should not raise
