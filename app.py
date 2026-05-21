"""Landing page for the Legal AI Model QA Workbench."""

import streamlit as st

st.set_page_config(page_title="Legal AI Model QA Workbench", layout="wide")

st.title("Legal AI Model QA Workbench")
st.subheader(
    "Simulated Contract-Intelligence QA for Extraction Accuracy, Error Analysis, and Cross-Functional Review"
)

st.write(
    "This portfolio project simulates how legal AI teams evaluate contract-term extraction quality "
    "using synthetic data, gold-standard labels, and structured QA metrics."
)

st.info(
    "Synthetic-data only: this app uses synthetic contract excerpts and does not include Workday, "
    "Evisort, customer, or other proprietary data."
)

st.warning(
    "No legal advice: this is a technical QA and product-evaluation demonstration, not legal counsel."
)

st.caption(
    "No paid APIs are used in this project. Use the left sidebar to navigate the full employer-facing walkthrough."
)


st.markdown("**Current maturity:** Portfolio MVP focused on evaluation workflow design (not a production deployment).")
