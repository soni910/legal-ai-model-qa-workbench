import pandas as pd
import streamlit as st

from utils.data_loader import load_gold_labels, load_model_outputs

st.set_page_config(page_title="Improvement Recommendations", layout="wide")

st.title("🛠️ Improvement Recommendations")
st.caption(
    "Actionable QA recommendations generated from the simulated evaluation dataset for portfolio demonstration."
)

st.info(
    "This page does **not** use a live AI model. Recommendations are generated from patterns in the "
    "synthetic `model_outputs.csv` evaluation dataset."
)

outputs_df = load_model_outputs()
labels_df = load_gold_labels()

frame = outputs_df.copy()
frame["score_numeric"] = pd.to_numeric(frame["score"], errors="coerce")
frame["confidence_numeric"] = pd.to_numeric(frame["confidence"], errors="coerce")
frame["error_type_clean"] = frame["error_type"].fillna("").astype(str).str.strip()
frame["source_match_status_clean"] = (
    frame["source_match_status"].fillna("unknown").astype(str).str.lower().str.strip()
)
frame["escalation_required_clean"] = (
    frame["escalation_required"].fillna("false").astype(str).str.lower().str.strip()
)

st.markdown("---")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Outputs", f"{len(frame):,}")
k2.metric("Error Rows", f"{(frame['error_type_clean'] != '').sum():,}")
k3.metric("Avg Score", f"{frame['score_numeric'].mean():.2f}" if not frame.empty else "0.00")
k4.metric(
    "High-Confidence Incorrect",
    f"{((frame['confidence_numeric'] >= 0.70) & (frame['score_numeric'] <= 0.25)).sum():,}",
)
k5.metric(
    "Source-Support Issues",
    f"{(frame['source_match_status_clean'].isin(['unsupported', 'partially_supported'])).sum():,}",
)

st.markdown("---")
st.subheader("Diagnostic Findings")

left, right = st.columns(2)

with left:
    st.markdown("### Common Error Types")
    error_summary = (
        frame[frame["error_type_clean"] != ""]
        .groupby("error_type_clean")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    if error_summary.empty:
        st.success("No error rows found in the current dataset slice.")
    else:
        st.dataframe(error_summary, use_container_width=True, hide_index=True)

    st.markdown("### Fields with Lowest Scores")
    lowest_fields = (
        frame.groupby("field_name", dropna=False)
        .agg(average_score=("score_numeric", "mean"), assessable_outputs=("score_numeric", "count"))
        .reset_index()
        .sort_values(["average_score", "assessable_outputs"], ascending=[True, False])
        .head(8)
    )
    if lowest_fields.empty:
        st.info("No field-level score data available.")
    else:
        lowest_fields["average_score"] = lowest_fields["average_score"].round(3)
        st.dataframe(lowest_fields, use_container_width=True, hide_index=True)

with right:
    st.markdown("### High-Confidence Incorrect Outputs")
    hc_incorrect = frame[(frame["confidence_numeric"] >= 0.70) & (frame["score_numeric"] <= 0.25)].copy()
    if hc_incorrect.empty:
        st.success("No high-confidence incorrect outputs detected.")
    else:
        st.dataframe(
            hc_incorrect[
                [
                    "output_id",
                    "run_id",
                    "field_name",
                    "match_status",
                    "score",
                    "confidence",
                    "error_type",
                    "severity",
                ]
            ].sort_values(["confidence", "score"], ascending=[False, True]),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("### Source-Support Problems")
    source_issues = frame[
        frame["source_match_status_clean"].isin(["unsupported", "partially_supported"])
    ].copy()
    source_summary = (
        source_issues.groupby("source_match_status_clean").size().reset_index(name="count")
        if not source_issues.empty
        else pd.DataFrame(columns=["source_match_status_clean", "count"])
    )
    if source_summary.empty:
        st.success("No source-support problems detected.")
    else:
        st.dataframe(source_summary, use_container_width=True, hide_index=True)

st.markdown("---")
st.subheader("Recommendation Playbook")
st.caption("Generated from recurring patterns in the simulated evaluation data.")

# Basic pattern signals
most_common_errors = error_summary["error_type_clean"].head(3).tolist() if not error_summary.empty else []
low_field_list = lowest_fields["field_name"].head(3).tolist() if not lowest_fields.empty else []
source_issue_count = len(source_issues)
hc_issue_count = len(hc_incorrect)
escalation_count = int((frame["escalation_required_clean"] == "true").sum())

r1, r2 = st.columns(2)

with r1:
    with st.container(border=True):
        st.markdown("### 1) Prompt / Instruction Improvements")
        st.markdown(
            f"""
- Prioritize prompts for error classes: **{', '.join(most_common_errors) if most_common_errors else 'none detected'}**.
- Add explicit steps for exception handling and party-role resolution when extracting obligations.
- Require answer + supporting source phrase pairs for each extracted field.
- For lower-performing fields (**{', '.join(low_field_list) if low_field_list else 'N/A'}**), add field-specific extraction guardrails.
            """
        )

    with st.container(border=True):
        st.markdown("### 2) Annotation-Guide Improvements")
        st.markdown(
            """
- Add annotation examples for ambiguous clauses and cross-reference-heavy clauses.
- Clarify how to label partial correctness vs. incorrect extraction outcomes.
- Expand guidance for when annotators should set legal SME escalation flags.
- Include positive/negative source-support examples to improve citation consistency.
            """
        )

    with st.container(border=True):
        st.markdown("### 3) Product-Design Improvements")
        st.markdown(
            f"""
- Add UI warnings for **high-confidence low-score outputs** (currently **{hc_issue_count}** detected).
- Surface source-support status prominently next to each extracted answer.
- Add field-level quality badges so reviewers can quickly target weak extraction domains.
- Add reviewer workflow shortcuts for filtering by severity and escalation-required rows.
            """
        )

with r2:
    with st.container(border=True):
        st.markdown("### 4) Data-Science Review Items")
        st.markdown(
            f"""
- Run error-focused analysis on top error types: **{', '.join(most_common_errors) if most_common_errors else 'none detected'}**.
- Audit confidence calibration where confidence ≥ 0.70 but score ≤ 0.25.
- Investigate low-performing fields: **{', '.join(low_field_list) if low_field_list else 'N/A'}**.
- Create targeted synthetic augmentation sets for unsupported/partially-supported source citations (**{source_issue_count}** rows).
            """
        )

    with st.container(border=True):
        st.markdown("### 5) Legal SME Escalation Triggers")
        st.markdown(
            f"""
- Escalate ambiguous outputs when clause interpretation could change contractual risk.
- Escalate monetary, liability-cap, and exception-extraction disagreements.
- Escalate recurring party-attribution errors in indemnity, termination, and assignment clauses.
- Current dataset marks **{escalation_count}** rows as escalation-required; use these as calibration examples.
            """
        )

    with st.container(border=True):
        st.markdown("### Implementation Note")
        st.write(
            "These recommendations are rule-based summaries derived from synthetic QA data patterns, "
            "not outputs from a production legal AI system."
        )
