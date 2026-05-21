import streamlit as st

st.set_page_config(page_title="Project Overview", layout="wide")

st.title("🧭 Project Overview")
st.caption(
    "Legal AI Model QA Workbench • Contract Intelligence Dataset, Evaluation Harness, Error Taxonomy, and Annotation Guide"
)

st.markdown("---")

left, right = st.columns([1.4, 1])

with left:
    st.markdown("## What this project is")
    st.markdown(
        """
This portfolio project simulates a real-world **Legal AI Model QA** workflow for contract intelligence.

It demonstrates how a legal AI product specialist or contract-intelligence analyst can evaluate extraction quality using:
- synthetic contract excerpts
- human-reviewed gold labels
- prompt/version run tracking
- structured error taxonomy
- source-text support checks
- confidence and severity analysis

The goal is to show a practical, recruiter-friendly QA framework that helps teams improve model reliability and reduce contractual risk.
        """
    )

with right:
    st.info(
        "**Synthetic Data Only**\n\n"
        "All records in this app are synthetic and created for portfolio demonstration. "
        "No client or confidential data is used."
    )
    st.warning(
        "**No Legal Advice**\n\n"
        "This project is a technical QA demonstration and does not provide legal advice."
    )

st.markdown("---")

st.markdown("## Why contract AI QA matters")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Risk Impact", "High", "Bad extraction can misstate obligations")
with col2:
    st.metric("Operational Value", "High", "Reliable outputs accelerate review")
with col3:
    st.metric("Trust Requirement", "Critical", "Stakeholders need explainable answers")

st.markdown(
    """
Contract AI outputs can directly influence legal, procurement, finance, and security decisions.
A robust QA process is essential to:
- detect false positives/false negatives before rollout
- catch party, time-period, and monetary misreads
- verify extracted answers are supported by source text
- identify high-confidence incorrect predictions
- prioritize fixes based on severity and escalation needs
    """
)

st.markdown("---")

st.markdown("## Skills demonstrated")
skills_left, skills_right = st.columns(2)
with skills_left:
    st.markdown(
        """
- ✅ Contract analysis
- ✅ Legal AI model evaluation
- ✅ Gold-standard labeling
- ✅ Error taxonomy design
        """
    )
with skills_right:
    st.markdown(
        """
- ✅ Source-text validation
- ✅ Prompt-version comparison
- ✅ Model improvement recommendations
- ✅ Legal/Product/Data-Science communication
        """
    )

st.markdown("---")

st.markdown("## How an employer should review this app")
with st.container(border=True):
    st.markdown(
        """
### Recommended review flow
1. **Dataset Browser**: confirm synthetic coverage across contract types and clause patterns.
2. **Gold Standard Labels**: inspect label quality, ambiguity flags, and SME-escalation signals.
3. **Prompt & Model Runs**: compare prompt versions and run metadata.
4. **Extraction Evaluation**: assess weighted quality (exact/partial/incorrect) and field-level performance.
5. **Error Taxonomy**: verify categorization discipline and severity handling.
6. **QA Dashboard**: review trend-style summaries and confidence calibration.
7. **Improvement Recommendations**: evaluate actionability of proposed instruction changes.
8. **Annotation Guide**: verify repeatable labeling standards and cross-functional clarity.

### What to look for
- structured evaluation thinking (not just model outputs)
- traceability from source text → labels → outputs → metrics
- practical prioritization of fixes by severity and escalation
- clear communication for legal, product, and data-science audiences
        """
    )

st.markdown("---")
st.success(
    "This page is intentionally designed as a recruiter-facing summary of domain understanding, QA rigor, and communication quality."
)
