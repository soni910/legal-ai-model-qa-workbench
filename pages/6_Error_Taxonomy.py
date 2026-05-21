import streamlit as st

from utils.data_loader import load_error_taxonomy

st.set_page_config(page_title="Error Taxonomy", layout="wide")

st.title("🧩 Error Taxonomy")
st.caption(
    "Structured error categories for legal-AI extraction QA, severity triage, and cross-functional improvement planning."
)

st.info(
    "A strong error taxonomy turns model mistakes into actionable signals for product, prompt, annotation, and legal-review workflows."
)

taxonomy_df = load_error_taxonomy()

st.markdown("---")

k1, k2, k3 = st.columns(3)
k1.metric("Error Types", f"{taxonomy_df['error_type'].nunique():,}")
k2.metric("High-Severity Types", f"{(taxonomy_df['typical_severity'].astype(str).str.lower() == 'high').sum():,}")
k3.metric("Escalation Paths", f"{taxonomy_df['escalation_guidance'].notna().sum():,}")

st.markdown("---")
st.subheader("Why error taxonomy matters")
st.markdown(
    """
In legal AI QA, raw accuracy alone is not enough. Error taxonomy matters because it helps teams:
- separate low-impact wording issues from high-risk interpretation failures
- triage errors consistently using severity and escalation context
- identify recurring failure patterns across fields, prompts, and runs
- convert repeated errors into process and product improvements

When recurring errors are tracked well, they become concrete inputs for:
- **product requirements** (UX warnings, review workflows, guardrails)
- **prompt improvements** (instruction specificity, exception handling, scope control)
- **annotation-guide updates** (clearer rules, better borderline examples)
- **legal SME review triggers** (ambiguity, liability, party attribution, monetary disputes)
    """
)

st.markdown("---")
st.subheader("Error Taxonomy Table")

table_cols = [
    "error_type",
    "definition",
    "example",
    "typical_severity",
    "escalation_guidance",
]

st.dataframe(
    taxonomy_df[table_cols].sort_values(["typical_severity", "error_type"]),
    width="stretch",
    hide_index=True,
)

st.markdown("---")
st.subheader("Error Type Drill-Down")
st.caption("Expand each category for reviewer-ready guidance.")

for _, row in taxonomy_df.sort_values("error_type").iterrows():
    severity = str(row["typical_severity"]).strip().lower()
    emoji = "🔴" if severity == "high" else "🟠" if severity == "medium" else "🟢"
    with st.expander(f"{emoji} {row['error_type']}"):
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("**Definition**")
            st.write(row["definition"])

            st.markdown("**Typical Severity**")
            st.write(row["typical_severity"])

        with c2:
            st.markdown("**Example**")
            st.write(row["example"])

            st.markdown("**Escalation Guidance**")
            st.write(row["escalation_guidance"])

st.markdown("---")
with st.container(border=True):
    st.markdown("### Practical QA usage")
    st.markdown(
        "Use this taxonomy alongside Extraction Evaluation and QA Dashboard views to prioritize high-risk failures, "
        "route escalations, and define next prompt/annotation/product actions."
    )
