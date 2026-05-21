import pandas as pd

from utils.evaluator import (
    accuracy_by_field,
    confidence_bucket,
    errors_by_type,
    high_confidence_incorrect_outputs,
    score_from_match_status,
)


def test_score_from_match_status_values() -> None:
    assert score_from_match_status("correct") == 1.0
    assert score_from_match_status("mostly_correct") == 0.75
    assert score_from_match_status("partial") == 0.5
    assert score_from_match_status("minimally_correct") == 0.25
    assert score_from_match_status("incorrect") == 0.0
    assert score_from_match_status("not_assessable") is None
    assert score_from_match_status("ambiguous") is None


def test_confidence_bucket_ranges() -> None:
    assert confidence_bucket(0.0) == "low"
    assert confidence_bucket(0.39) == "low"
    assert confidence_bucket(0.40) == "medium"
    assert confidence_bucket(0.69) == "medium"
    assert confidence_bucket(0.70) == "high"
    assert confidence_bucket(1.0) == "high"


def test_high_confidence_incorrect_detection() -> None:
    frame = pd.DataFrame(
        [
            {"output_id": "O1", "confidence": 0.9, "score": 0.0},
            {"output_id": "O2", "confidence": 0.75, "score": 0.25},
            {"output_id": "O3", "confidence": 0.8, "score": 0.5},
            {"output_id": "O4", "confidence": 0.2, "score": 0.0},
        ]
    )
    flagged = high_confidence_incorrect_outputs(frame)
    assert set(flagged["output_id"].tolist()) == {"O1", "O2"}


def test_accuracy_by_field() -> None:
    frame = pd.DataFrame(
        [
            {"field_name": "governing_law", "score": 1.0},
            {"field_name": "governing_law", "score": 0.5},
            {"field_name": "notice_period", "score": 0.0},
        ]
    )
    summary = accuracy_by_field(frame)
    row = summary[summary["field_name"] == "governing_law"].iloc[0]
    assert row["assessable_outputs"] == 2
    assert row["average_score"] == 0.75


def test_errors_by_type_summary() -> None:
    frame = pd.DataFrame(
        [
            {"error_type": "False positive"},
            {"error_type": "False positive"},
            {"error_type": "Monetary error"},
            {"error_type": ""},
        ]
    )
    summary = errors_by_type(frame)
    counts = dict(zip(summary["error_type"], summary["count"]))
    assert counts["False positive"] == 2
    assert counts["Monetary error"] == 1
