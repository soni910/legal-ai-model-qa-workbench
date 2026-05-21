"""Chart helpers for Streamlit/Altair visualizations."""

import altair as alt
import pandas as pd


def _empty_guard(data: pd.DataFrame) -> bool:
    return data is None or data.empty


def chart_accuracy_by_field(data: pd.DataFrame) -> alt.Chart | None:
    if _empty_guard(data):
        return None
    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("average_score:Q", title="Average Score", scale=alt.Scale(domain=[0, 1])),
            y=alt.Y("field_name:N", sort="-x", title="Field"),
            tooltip=["field_name", "assessable_outputs", "average_score", "exact_accuracy"],
        )
        .properties(title="Accuracy by Field")
    )


def chart_accuracy_by_contract_type(data: pd.DataFrame) -> alt.Chart | None:
    if _empty_guard(data):
        return None
    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("average_score:Q", title="Average Score", scale=alt.Scale(domain=[0, 1])),
            y=alt.Y("contract_type:N", sort="-x", title="Contract Type"),
            tooltip=["contract_type", "assessable_outputs", "average_score", "exact_accuracy"],
        )
        .properties(title="Accuracy by Contract Type")
    )


def chart_accuracy_by_prompt_version(data: pd.DataFrame) -> alt.Chart | None:
    if _empty_guard(data):
        return None
    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("prompt_version:N", title="Prompt Version"),
            y=alt.Y("average_score:Q", title="Average Score", scale=alt.Scale(domain=[0, 1])),
            tooltip=["prompt_version", "assessable_outputs", "average_score", "exact_accuracy"],
        )
        .properties(title="Accuracy by Prompt Version")
    )


def chart_errors_by_type(data: pd.DataFrame) -> alt.Chart | None:
    if _empty_guard(data):
        return None
    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("count:Q", title="Count"),
            y=alt.Y("error_type:N", sort="-x", title="Error Type"),
            tooltip=["error_type", "count"],
        )
        .properties(title="Errors by Type")
    )


def chart_severity_distribution(data: pd.DataFrame) -> alt.Chart | None:
    if _empty_guard(data):
        return None
    return (
        alt.Chart(data)
        .mark_arc(innerRadius=40)
        .encode(
            theta=alt.Theta("count:Q", title="Count"),
            color=alt.Color("severity:N", title="Severity"),
            tooltip=["severity", "count"],
        )
        .properties(title="Severity Distribution")
    )


def chart_confidence_calibration(data: pd.DataFrame) -> alt.Chart | None:
    if _empty_guard(data):
        return None
    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("confidence_bucket:N", title="Confidence Bucket"),
            y=alt.Y("average_score:Q", title="Average Score", scale=alt.Scale(domain=[0, 1])),
            tooltip=["confidence_bucket", "assessable_outputs", "average_score", "exact_accuracy"],
        )
        .properties(title="Confidence Calibration")
    )


def chart_source_support(data: pd.DataFrame) -> alt.Chart | None:
    if _empty_guard(data):
        return None
    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("count:Q", title="Count"),
            y=alt.Y("source_match_status:N", sort="-x", title="Source Match Status"),
            tooltip=["source_match_status", "count"],
        )
        .properties(title="Source Support Summary")
    )


def chart_escalation_distribution(data: pd.DataFrame) -> alt.Chart | None:
    if _empty_guard(data):
        return None
    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("escalation_required:N", title="Escalation Required"),
            y=alt.Y("count:Q", title="Count"),
            tooltip=["escalation_required", "count"],
        )
        .properties(title="Escalation Distribution")
    )
