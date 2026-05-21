import pandas as pd
import streamlit as st

from utils.data_loader import load_gold_labels, load_model_outputs

st.set_page_config(page_title="Extraction Evaluation", layout="wide")

st.title("📈 Extraction Evaluation")
st.caption(
    "Compare simulated model outputs against human-reviewed gold labels with filterable QA diagnostics."
)

st.info(
    "Portfolio note: this evaluation uses synthetic data and simulated outputs to demonstrate QA methodology."
)

outputs_df = load_model_outputs()
labels_df = load_gold_labels()

merged_df = outputs_df.merge(
    labels_df[["label_id", "gold_answer", "gold_source_text", "answer_status", "requires_legal_sme"]],
    on="label_id",
    how="left",
)

merged_df["score_numeric"] = pd.to_numeric(merged_df["score"], errors="coerce")

st.markdown("---")
st.subheader("Filters")

c1, c2, c3, c4 = st.columns(4)
c5, c6, c7 = st.columns(3)

field_options = ["All"] + sorted(merged_df["field_name"].dropna().astype(str).unique().tolist())
match_options = ["All"] + sorted(merged_df["match_status"].dropna().astype(str).unique().tolist())
error_options = ["All"] + sorted(
    [v for v in merged_df["error_type"].dropna().astype(str).unique().tolist() if v.strip()]
)
severity_options = ["All"] + sorted(merged_df["severity"].dropna().astype(str).unique().tolist())
esc_options = ["All"] + sorted(
    merged_df["escalation_required"].dropna().astype(str).str.lower().unique().tolist()
)
source_options = ["All"] + sorted(
    merged_df["source_match_status"].dropna().astype(str).unique().tolist()
)
run_options = ["All"] + sorted(merged_df["run_id"].dropna().astype(str).unique().tolist())

selected_field = c1.selectbox("Field Name", field_options)
selected_match = c2.selectbox("Match Status", match_options)
selected_error = c3.selectbox("Error Type", error_options)
selected_severity = c4.selectbox("Severity", severity_options)
selected_esc = c5.selectbox("Escalation Required", esc_options)
selected_source = c6.selectbox("Source Match Status", source_options)
selected_run = c7.selectbox("Run ID", run_options)

filtered_df = merged_df.copy()
if selected_field != "All":
    filtered_df = filtered_df[filtered_df["field_name"] == selected_field]
if selected_match != "All":
    filtered_df = filtered_df[filtered_df["match_status"] == selected_match]
if selected_error != "All":
    filtered_df = filtered_df[filtered_df["error_type"] == selected_error]
if selected_severity != "All":
    filtered_df = filtered_df[filtered_df["severity"] == selected_severity]
if selected_esc != "All":
    filtered_df = filtered_df[
        filtered_df["escalation_required"].astype(str).str.lower() == selected_esc
    ]
if selected_source != "All":
    filtered_df = filtered_df[filtered_df["source_match_status"] == selected_source]
if selected_run != "All":
    filtered_df = filtered_df[filtered_df["run_id"] == selected_run]

st.markdown("---")
st.subheader("Summary Metrics")

total_outputs = len(filtered_df)
assessable = filtered_df[filtered_df["score_numeric"].notna()]
average_score = float(assessable["score_numeric"].mean()) if not assessable.empty else 0.0
exact_accuracy = float((assessable["score_numeric"] == 1.0).mean()) if not assessable.empty else 0.0
high_sev_count = int((filtered_df["severity"].astype(str).str.lower() == "high").sum())
esc_count = int((filtered_df["escalation_required"].astype(str).str.lower() == "true").sum())

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total Outputs", f"{total_outputs:,}")
m2.metric("Average Score", f"{average_score:.2f}")
m3.metric("Exact Accuracy", f"{exact_accuracy:.1%}")
m4.metric("High-Severity Errors", f"{high_sev_count:,}")
m5.metric("Escalation-Required", f"{esc_count:,}")

st.markdown("---")
st.subheader("Detailed Comparison Table")

if filtered_df.empty:
    st.warning("No rows match the selected filters.")
else:
    display_columns = [
        "contract_id",
        "excerpt_id",
        "field_name",
        "gold_answer",
        "ai_answer",
        "gold_source_text",
        "ai_source_text",
        "confidence",
        "match_status",
        "score",
        "error_type",
        "severity",
        "suggested_instruction_fix",
    ]

    st.dataframe(
        filtered_df[display_columns].sort_values(["run_id", "contract_id", "excerpt_id", "field_name"]),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Use this comparison to inspect extraction disagreements, source-support gaps, and practical instruction-fix opportunities."
    )
