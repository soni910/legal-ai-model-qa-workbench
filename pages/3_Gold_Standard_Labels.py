import streamlit as st

from utils.data_loader import load_gold_labels

st.set_page_config(page_title="Gold Standard Labels", layout="wide")

st.title("🏷️ Gold Standard Labels")
st.caption("Human-reviewed reference answers used to evaluate extraction quality.")

st.info(
    "Gold-standard labels represent the human-reviewed correct answers for each excerpt/field pairing. "
    "They are the benchmark for scoring model outputs."
)

labels_df = load_gold_labels()

st.markdown("---")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Labels", f"{len(labels_df):,}")
m2.metric("Unique Fields", f"{labels_df['field_name'].nunique():,}")
m3.metric(
    "Requires Legal SME",
    f"{(labels_df['requires_legal_sme'].astype(str).str.lower() == 'true').sum():,}",
)
m4.metric(
    "Ambiguous Labels",
    f"{(labels_df['ambiguity_flag'].astype(str).str.lower() == 'true').sum():,}",
)

st.markdown("---")
st.markdown("### Filters")

f1, f2, f3, f4 = st.columns(4)

field_options = ["All"] + sorted(labels_df["field_name"].dropna().astype(str).unique().tolist())
status_options = ["All"] + sorted(labels_df["answer_status"].dropna().astype(str).unique().tolist())
legal_sme_options = ["All"] + sorted(
    labels_df["requires_legal_sme"].dropna().astype(str).str.lower().unique().tolist()
)
ambiguity_options = ["All"] + sorted(
    labels_df["ambiguity_flag"].dropna().astype(str).str.lower().unique().tolist()
)

selected_field = f1.selectbox("Field Name", field_options)
selected_status = f2.selectbox("Answer Status", status_options)
selected_legal_sme = f3.selectbox("Requires Legal SME", legal_sme_options)
selected_ambiguity = f4.selectbox("Ambiguity Flag", ambiguity_options)

filtered_df = labels_df.copy()
if selected_field != "All":
    filtered_df = filtered_df[filtered_df["field_name"] == selected_field]
if selected_status != "All":
    filtered_df = filtered_df[filtered_df["answer_status"] == selected_status]
if selected_legal_sme != "All":
    filtered_df = filtered_df[
        filtered_df["requires_legal_sme"].astype(str).str.lower() == selected_legal_sme
    ]
if selected_ambiguity != "All":
    filtered_df = filtered_df[
        filtered_df["ambiguity_flag"].astype(str).str.lower() == selected_ambiguity
    ]

st.markdown("---")
st.markdown("### Labels Table")

view_cols = [
    "label_id",
    "excerpt_id",
    "contract_id",
    "field_name",
    "answer_status",
    "requires_legal_sme",
    "ambiguity_flag",
    "gold_answer",
]


def highlight_legal_sme(row):
    is_sme = str(row["requires_legal_sme"]).strip().lower() == "true"
    color = "background-color: #fff3cd" if is_sme else ""
    return [color] * len(row)

if filtered_df.empty:
    st.warning("No labels match the current filter set.")
else:
    st.dataframe(
        filtered_df[view_cols]
        .sort_values(["requires_legal_sme", "ambiguity_flag", "label_id"], ascending=[False, False, True])
        .style.apply(highlight_legal_sme, axis=1),
        use_container_width=True,
        hide_index=True,
    )

st.caption("Rows highlighted in soft yellow require legal SME review.")

st.markdown("---")
st.markdown("### Label Detail")

if not filtered_df.empty:
    selected_label = st.selectbox(
        "Select a label_id to inspect source grounding",
        filtered_df["label_id"].astype(str).tolist(),
    )
    row = filtered_df[filtered_df["label_id"].astype(str) == selected_label].iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"**Field Name**  \n{row['field_name']}")
    c2.markdown(f"**Answer Status**  \n{row['answer_status']}")
    c3.markdown(f"**Requires Legal SME**  \n{row['requires_legal_sme']}")
    c4.markdown(f"**Ambiguity Flag**  \n{row['ambiguity_flag']}")

    with st.container(border=True):
        st.markdown("**Gold Answer**")
        st.write(row["gold_answer"])

    with st.container(border=True):
        st.markdown("**Gold Source Text**")
        st.write(row["gold_source_text"])

    if str(row["requires_legal_sme"]).strip().lower() == "true":
        st.warning("This label is flagged for legal SME review.")
