from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Annotation Guide", layout="wide")

st.title("📝 Annotation Guide")
st.caption(
    "Employer-facing annotation and escalation standards for synthetic legal-AI extraction QA."
)

st.info(
    "This guide applies to synthetic QA data in this portfolio project and is designed to demonstrate practical review rigor."
)

guide_path = Path(__file__).resolve().parent.parent / "docs" / "annotation_and_escalation_guide.md"

if not guide_path.exists():
    st.error("Guide file not found: docs/annotation_and_escalation_guide.md")
else:
    guide_text = guide_path.read_text(encoding="utf-8")

    with st.container(border=True):
        st.markdown("### How to use this page")
        st.markdown(
            "Use this as the operational rubric for evaluating extraction outputs, assigning error/severity labels, and making escalation decisions."
        )

    st.markdown("---")
    st.markdown(guide_text)
