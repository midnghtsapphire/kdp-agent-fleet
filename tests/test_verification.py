"""Tests for independent verification layer."""

from src.verification import verify_package, impact_analysis


def test_impact_finds_relevant():
    checks = ["manuscript present", "cover present", "title length"]
    impacted = impact_analysis("updated manuscript", checks)
    assert "manuscript present" in impacted


def test_verify_fails_missing():
    result = verify_package({})
    assert result.status == "fail"
    assert any(f["check"] == "manuscript present" for f in result.failures)


def test_verify_passes_complete():
    pkg = {
        "manuscript": "book.docx",
        "cover": "cover.jpg",
        "metadata": {"title": "Test", "keywords": ["a", "b"]},
    }
    result = verify_package(pkg)
    assert result.status == "pass"


def test_auto_heal_suggestion_on_fail():
    result = verify_package({})
    assert result.auto_heal_suggestions
