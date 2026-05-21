import streamlit as st

from utils.charts import (
    chart_accuracy_by_contract_type,
    chart_accuracy_by_field,
    chart_accuracy_by_prompt_version,
    chart_confidence_calibration,
    chart_errors_by_type,
    chart_escalation_distribution,
    chart_severity_distribution,
    chart_source_support,
)
from utils.data_loader import load_contracts, load_gold_labels, load_model_outputs, load_model_runs
from utils.evaluator import (
    accuracy_by_contract_type,
    accuracy_by_field,
    accuracy_by_prompt_version,
    confidence_calibration,
    errors_by_type,
    escalation_summary,
    high_confidence_incorrect_outputs,
    severity_summary,
    source_support_summary,
    summarize_overall_performance,
)

st.set_page_config(page_title="QA Dashboard", layout="wide")

st.title("📊 QA Dashboard")
st.caption(
    "Portfolio QA analytics for synthetic contract-extraction evaluation: score health, error risk, and escalation signals."
)
st.info(
    "All metrics are computed from synthetic evaluation artifacts for demonstration. "
    "No client data is used and this dashboard does not provide legal advice."
)

outputs_df = load_model_outputs()
contracts_df = load_contracts()
runs_df = load_model_runs()
labels_df = load_gold_labels()

# Join outputs to labels so drill-down tables can include gold answers.
outputs_with_labels = outputs_df.merge(
    labels_df[["label_id", "gold_answer", "gold_source_text"]], on="label_id", how="left"
)

overall = summarize_overall_performance(outputs_df)

st.markdown("---")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Overall Weighted Score", f"{overall['average_score']:.2f}")
k2.metric("Exact Accuracy", f"{overall['exact_accuracy']:.1%}")
k3.metric("Total Evaluated Outputs", f"{overall['total_outputs']:,}")
k4.metric("High-Severity Errors", f"{overall['high_severity_count']:,}")
k5.metric("Escalation-Required", f"{overall['escalation_required_count']:,}")

st.markdown("---")
st.subheader("Performance & Risk Charts")

field_df = accuracy_by_field(outputs_df)
contract_df = accuracy_by_contract_type(outputs_df, contracts_df)
prompt_df = accuracy_by_prompt_version(outputs_df, runs_df)
error_df = errors_by_type(outputs_df)
severity_df = severity_summary(outputs_df)
calib_df = confidence_calibration(outputs_df)
source_df = source_support_summary(outputs_df)
escalation_df = escalation_summary(outputs_df)

r1c1, r1c2 = st.columns(2)
with r1c1:
    st.markdown("#### Accuracy by Field")
    chart = chart_accuracy_by_field(field_df)
    if chart is not None:
        st.altair_chart(chart, width="stretch")
    else:
        st.info("No data available for field-level accuracy.")

with r1c2:
    st.markdown("#### Accuracy by Contract Type")
    chart = chart_accuracy_by_contract_type(contract_df)
    if chart is not None:
        st.altair_chart(chart, width="stretch")
    else:
        st.info("No data available for contract-type accuracy.")

r2c1, r2c2 = st.columns(2)
with r2c1:
    st.markdown("#### Accuracy by Prompt Version")
    chart = chart_accuracy_by_prompt_version(prompt_df)
    if chart is not None:
        st.altair_chart(chart, width="stretch")
    else:
        st.info("No data available for prompt-version accuracy.")

with r2c2:
    st.markdown("#### Error Type Distribution")
    chart = chart_errors_by_type(error_df)
    if chart is not None:
        st.altair_chart(chart, width="stretch")
    else:
        st.info("No data available for error-type distribution.")

r3c1, r3c2 = st.columns(2)
with r3c1:
    st.markdown("#### Severity Distribution")
    chart = chart_severity_distribution(severity_df)
    if chart is not None:
        st.altair_chart(chart, width="stretch")
    else:
        st.info("No data available for severity distribution.")

with r3c2:
    st.markdown("#### Confidence Calibration")
    chart = chart_confidence_calibration(calib_df)
    if chart is not None:
        st.altair_chart(chart, width="stretch")
    else:
        st.info("No data available for confidence calibration.")

r4c1, r4c2 = st.columns(2)
with r4c1:
    st.markdown("#### Source Support Status")
    chart = chart_source_support(source_df)
    if chart is not None:
        st.altair_chart(chart, width="stretch")
    else:
        st.info("No data available for source-support status.")

with r4c2:
    st.markdown("#### Escalation Distribution")
    chart = chart_escalation_distribution(escalation_df)
    if chart is not None:
        st.altair_chart(chart, width="stretch")
    else:
        st.info("No data available for escalation distribution.")

st.markdown("---")
st.subheader("High-Confidence Incorrect Outputs")
st.caption(
    "High-confidence wrong answers are high-risk in legal AI because they can appear trustworthy while misrepresenting obligations."
)

high_risk = high_confidence_incorrect_outputs(outputs_with_labels)
if high_risk.empty:
    st.success("No high-confidence incorrect outputs detected in the current dataset.")
else:
    table_cols = [
        "contract_id",
        "excerpt_id",
        "field_name",
        "ai_answer",
        "gold_answer",
        "confidence",
        "error_type",
        "severity",
        "suggested_instruction_fix",
    ]
    st.dataframe(
        high_risk[table_cols].sort_values(["confidence", "severity"], ascending=[False, True]),
        width="stretch",
        hide_index=True,
    )
