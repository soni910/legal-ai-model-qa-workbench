import streamlit as st

st.set_page_config(page_title="Project Overview", layout="wide")

st.title("🧭 Project Overview")
st.caption(
    "Legal AI Model QA Workbench • Employer-facing portfolio for simulated contract-intelligence evaluation"
)

st.markdown("---")

left, right = st.columns([1.4, 1])

with left:
    st.markdown("## What this project is")
    st.markdown(
        """
This is a **simulated contract-intelligence QA workbench**.

It demonstrates how a legal AI product specialist or contract analyst can evaluate extraction quality using:
- synthetic contract excerpts
- gold-standard human-reviewed labels
- model output comparisons
- structured error taxonomy
- escalation workflows for legal/product/data-science teams

The focus is practical QA rigor for contract term extraction, not production legal automation.
        """
    )

with right:
    st.info(
        "**Synthetic Data Only**\n\n"
        "All data is synthetic. No proprietary Workday, Evisort, customer, or confidential data is used."
    )
    st.warning(
        "**No Legal Advice**\n\n"
        "This project is for QA/product demonstration and does not provide legal advice."
    )
    st.caption("No paid APIs are used.")

st.markdown("---")

st.markdown("## Why contract AI QA matters")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Risk Exposure", "High", "Incorrect extraction can distort obligations")
with col2:
    st.metric("Business Value", "High", "Reliable extraction accelerates review")
with col3:
    st.metric("Trust Requirement", "Critical", "Outputs must be evidence-backed")

st.markdown(
    """
Strong QA helps teams identify high-confidence errors, monitor source support quality,
track prompt-version impact, and route ambiguous/high-risk cases for escalation.
    """
)

st.markdown("---")
st.markdown("## Skills Demonstrated")
sl, sr = st.columns(2)
with sl:
    st.markdown(
        """
- ✅ contract analysis
- ✅ legal AI model evaluation
- ✅ annotation guide drafting
- ✅ error taxonomy design
        """
    )
with sr:
    st.markdown(
        """
- ✅ product/legal/data-science communication
- ✅ QA dashboard design
- ✅ synthetic dataset design
- ✅ model-instruction improvement
        """
    )

st.markdown("---")

st.markdown("---")
st.markdown("## Current maturity (honest scope)")
st.markdown("This is a portfolio MVP. It demonstrates QA workflow design and cross-functional review, not a production legal AI platform.")

st.markdown("## How an employer should review this")
with st.container(border=True):
    st.markdown(
        """
1. **Start with Project Overview** to understand constraints and evaluation goals.
2. **Review Synthetic Dataset** in Dataset Browser to inspect coverage and scenario variety.
3. **Review Gold Standard Labels** to assess rubric discipline and ambiguity handling.
4. **Review Extraction Evaluation** to inspect output-vs-gold scoring quality.
5. **Review QA Dashboard** for risk signals, trends, and high-confidence incorrect outputs.
6. **Review Annotation Guide** for operational consistency and escalation readiness.
        """
    )

st.success(
    "This portfolio demonstrates contract-term extraction QA workflows with synthetic data, structured scoring, and practical escalation design."
)
