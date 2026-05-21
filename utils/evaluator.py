"""Evaluation helpers for extraction quality metrics."""

from __future__ import annotations

from typing import Any

import pandas as pd


SCORE_MAP: dict[str, float | None] = {
    "correct": 1.0,
    "mostly_correct": 0.75,
    "partial": 0.5,
    "minimally_correct": 0.25,
    "incorrect": 0.0,
    "not_assessable": None,
    "ambiguous": None,
}


def normalize_text(value: Any) -> str:
    """Normalize free-text values for robust comparisons."""
    if value is None or pd.isna(value):
        return ""
    return str(value).strip().lower()


def score_from_match_status(match_status: Any) -> float | None:
    """Map match-status labels to numeric scores."""
    normalized = normalize_text(match_status)
    return SCORE_MAP.get(normalized)


def _ensure_score_column(model_outputs_df: pd.DataFrame) -> pd.DataFrame:
    frame = model_outputs_df.copy()
    if "score" in frame.columns:
        frame["score_numeric"] = pd.to_numeric(frame["score"], errors="coerce")
    else:
        frame["score_numeric"] = frame.get("match_status", pd.Series(dtype=object)).map(
            score_from_match_status
        )
    return frame


def summarize_overall_performance(model_outputs_df: pd.DataFrame) -> dict[str, Any]:
    if model_outputs_df.empty:
        return {
            "total_outputs": 0,
            "assessable_outputs": 0,
            "average_score": 0.0,
            "exact_accuracy": 0.0,
            "high_severity_count": 0,
            "escalation_required_count": 0,
        }

    frame = _ensure_score_column(model_outputs_df)
    assessable = frame[frame["score_numeric"].notna()]

    total_outputs = len(frame)
    assessable_outputs = len(assessable)
    average_score = float(assessable["score_numeric"].mean()) if assessable_outputs else 0.0
    exact_accuracy = (
        float((assessable["score_numeric"] == 1.0).mean()) if assessable_outputs else 0.0
    )
    high_severity_count = int((frame.get("severity", "").astype(str).str.lower() == "high").sum())
    escalation_required_count = int(
        (frame.get("escalation_required", "").astype(str).str.lower() == "true").sum()
    )

    return {
        "total_outputs": total_outputs,
        "assessable_outputs": assessable_outputs,
        "average_score": round(average_score, 4),
        "exact_accuracy": round(exact_accuracy, 4),
        "high_severity_count": high_severity_count,
        "escalation_required_count": escalation_required_count,
    }


def accuracy_by_field(model_outputs_df: pd.DataFrame) -> pd.DataFrame:
    if model_outputs_df.empty:
        return pd.DataFrame(columns=["field_name", "assessable_outputs", "average_score", "exact_accuracy"])
    frame = _ensure_score_column(model_outputs_df)
    assessable = frame[frame["score_numeric"].notna()]
    if assessable.empty:
        return pd.DataFrame(columns=["field_name", "assessable_outputs", "average_score", "exact_accuracy"])
    out = (
        assessable.groupby("field_name", dropna=False)
        .agg(
            assessable_outputs=("score_numeric", "count"),
            average_score=("score_numeric", "mean"),
            exact_accuracy=("score_numeric", lambda s: (s == 1.0).mean()),
        )
        .reset_index()
    )
    out["average_score"] = out["average_score"].round(4)
    out["exact_accuracy"] = out["exact_accuracy"].round(4)
    return out


def accuracy_by_contract_type(model_outputs_df: pd.DataFrame, contracts_df: pd.DataFrame) -> pd.DataFrame:
    if model_outputs_df.empty or contracts_df.empty:
        return pd.DataFrame(columns=["contract_type", "assessable_outputs", "average_score", "exact_accuracy"])
    frame = _ensure_score_column(model_outputs_df)
    merged = frame.merge(contracts_df[["contract_id", "contract_type"]], on="contract_id", how="left")
    assessable = merged[merged["score_numeric"].notna()]
    if assessable.empty:
        return pd.DataFrame(columns=["contract_type", "assessable_outputs", "average_score", "exact_accuracy"])
    out = (
        assessable.groupby("contract_type", dropna=False)
        .agg(
            assessable_outputs=("score_numeric", "count"),
            average_score=("score_numeric", "mean"),
            exact_accuracy=("score_numeric", lambda s: (s == 1.0).mean()),
        )
        .reset_index()
    )
    out["average_score"] = out["average_score"].round(4)
    out["exact_accuracy"] = out["exact_accuracy"].round(4)
    return out


def accuracy_by_prompt_version(model_outputs_df: pd.DataFrame, model_runs_df: pd.DataFrame) -> pd.DataFrame:
    if model_outputs_df.empty or model_runs_df.empty:
        return pd.DataFrame(columns=["prompt_version", "assessable_outputs", "average_score", "exact_accuracy"])
    frame = _ensure_score_column(model_outputs_df)
    merged = frame.merge(model_runs_df[["run_id", "prompt_version"]], on="run_id", how="left")
    assessable = merged[merged["score_numeric"].notna()]
    if assessable.empty:
        return pd.DataFrame(columns=["prompt_version", "assessable_outputs", "average_score", "exact_accuracy"])
    out = (
        assessable.groupby("prompt_version", dropna=False)
        .agg(
            assessable_outputs=("score_numeric", "count"),
            average_score=("score_numeric", "mean"),
            exact_accuracy=("score_numeric", lambda s: (s == 1.0).mean()),
        )
        .reset_index()
    )
    out["average_score"] = out["average_score"].round(4)
    out["exact_accuracy"] = out["exact_accuracy"].round(4)
    return out


def errors_by_type(model_outputs_df: pd.DataFrame) -> pd.DataFrame:
    if model_outputs_df.empty or "error_type" not in model_outputs_df.columns:
        return pd.DataFrame(columns=["error_type", "count"])
    frame = model_outputs_df.copy()
    frame["error_type"] = frame["error_type"].fillna("").astype(str).str.strip()
    frame = frame[frame["error_type"] != ""]
    if frame.empty:
        return pd.DataFrame(columns=["error_type", "count"])
    return frame.groupby("error_type").size().reset_index(name="count").sort_values("count", ascending=False)


def severity_summary(model_outputs_df: pd.DataFrame) -> pd.DataFrame:
    if model_outputs_df.empty or "severity" not in model_outputs_df.columns:
        return pd.DataFrame(columns=["severity", "count"])
    frame = model_outputs_df.copy()
    frame["severity"] = frame["severity"].fillna("unknown").astype(str).str.lower().str.strip()
    return frame.groupby("severity").size().reset_index(name="count").sort_values("count", ascending=False)


def escalation_summary(model_outputs_df: pd.DataFrame) -> pd.DataFrame:
    if model_outputs_df.empty or "escalation_required" not in model_outputs_df.columns:
        return pd.DataFrame(columns=["escalation_required", "count"])
    frame = model_outputs_df.copy()
    frame["escalation_required"] = frame["escalation_required"].fillna("false").astype(str).str.lower().str.strip()
    return frame.groupby("escalation_required").size().reset_index(name="count")


def source_support_summary(model_outputs_df: pd.DataFrame) -> pd.DataFrame:
    if model_outputs_df.empty or "source_match_status" not in model_outputs_df.columns:
        return pd.DataFrame(columns=["source_match_status", "count"])
    frame = model_outputs_df.copy()
    frame["source_match_status"] = (
        frame["source_match_status"].fillna("unknown").astype(str).str.lower().str.strip()
    )
    return frame.groupby("source_match_status").size().reset_index(name="count").sort_values("count", ascending=False)


def confidence_bucket(confidence: Any) -> str:
    try:
        value = float(confidence)
    except (TypeError, ValueError):
        return "unknown"
    if value < 0 or value > 1:
        return "unknown"
    if value <= 0.39:
        return "low"
    if value <= 0.69:
        return "medium"
    return "high"


def confidence_calibration(model_outputs_df: pd.DataFrame) -> pd.DataFrame:
    if model_outputs_df.empty:
        return pd.DataFrame(columns=["confidence_bucket", "assessable_outputs", "average_score", "exact_accuracy"])
    frame = _ensure_score_column(model_outputs_df)
    frame["confidence_bucket"] = frame.get("confidence", pd.Series(dtype=float)).apply(confidence_bucket)
    assessable = frame[frame["score_numeric"].notna()]
    if assessable.empty:
        return pd.DataFrame(columns=["confidence_bucket", "assessable_outputs", "average_score", "exact_accuracy"])
    out = (
        assessable.groupby("confidence_bucket")
        .agg(
            assessable_outputs=("score_numeric", "count"),
            average_score=("score_numeric", "mean"),
            exact_accuracy=("score_numeric", lambda s: (s == 1.0).mean()),
        )
        .reset_index()
    )
    return out


def high_confidence_incorrect_outputs(model_outputs_df: pd.DataFrame) -> pd.DataFrame:
    if model_outputs_df.empty:
        return pd.DataFrame(columns=list(model_outputs_df.columns))
    frame = _ensure_score_column(model_outputs_df)
    frame["confidence_bucket"] = frame.get("confidence", pd.Series(dtype=float)).apply(confidence_bucket)
    return frame[(frame["confidence_bucket"] == "high") & (frame["score_numeric"] <= 0.25)].copy()


def improvement_recommendations(model_outputs_df: pd.DataFrame) -> pd.DataFrame:
    if model_outputs_df.empty or "error_type" not in model_outputs_df.columns:
        return pd.DataFrame(columns=["error_type", "count", "recommended_instruction"])

    recommendation_map = {
        "false positive": "Constrain extraction to explicit clause language and reject unsupported inferences.",
        "false negative": "Add checklist-based extraction to ensure required fields are not skipped.",
        "scope error": "Require party/scope qualifiers in the answer and verify clause boundaries.",
        "party error": "Add explicit step to resolve obligation owner before final answer.",
        "time-period error": "Parse durations and effective windows explicitly before composing output.",
        "monetary error": "Validate currency, units, and numeric normalization before returning amounts.",
        "exception error": "Extract carve-outs alongside base rule and label each exception clearly.",
        "cross-reference error": "Follow referenced sections and merge exceptions into final extraction.",
        "source support error": "Require quoted supporting text directly tied to each extracted value.",
        "ambiguity escalation": "When ambiguity indicators are present, output escalation_required=true and explain uncertainty.",
    }

    frame = model_outputs_df.copy()
    frame["error_type_norm"] = frame.get("error_type", "").fillna("").astype(str).str.strip().str.lower()
    frame = frame[frame["error_type_norm"] != ""]
    if frame.empty:
        return pd.DataFrame(columns=["error_type", "count", "recommended_instruction"])

    out = frame.groupby("error_type_norm").size().reset_index(name="count")
    out["recommended_instruction"] = out["error_type_norm"].map(recommendation_map).fillna(
        "Review recurring errors and tighten extraction instructions accordingly."
    )
    out = out.rename(columns={"error_type_norm": "error_type"}).sort_values("count", ascending=False)
    return out
