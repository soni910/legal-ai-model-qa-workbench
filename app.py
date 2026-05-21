"""Landing page for the Legal AI Model QA Workbench."""

import streamlit as st

st.set_page_config(page_title="Legal AI Model QA Workbench", layout="wide")

st.title("Legal AI Model QA Workbench")
st.subheader(
    "Contract Intelligence Dataset, Evaluation Harness, Error Taxonomy, and Annotation Guide"
)

st.write(
    "This portfolio app demonstrates a beginner-friendly workflow for evaluating "
    "AI extraction quality on synthetic contract excerpts."
)

st.info(
    "Synthetic-data disclaimer: This project uses synthetic contract data only. "
    "No client or confidential data should be added."
)

st.warning(
    "No-legal-advice disclaimer: This project is for technical QA and product "
    "evaluation purposes only and does not provide legal advice."
)

st.markdown(
    "Use the left sidebar to navigate between pages for dataset browsing, labels, "
    "model runs, evaluation summaries, taxonomy views, and annotation guidance."
)
