import pandas as pd
import streamlit as st

from utils.data_loader import load_contracts, load_excerpts

st.set_page_config(page_title="Dataset Browser", layout="wide")

st.title("📚 Dataset Browser")
st.caption("Explore synthetic contracts and excerpts with filterable, review-friendly views.")

st.info(
    "Synthetic-data disclaimer: all records shown are synthetic and for QA portfolio demonstration only."
)

contracts_df = load_contracts()
excerpts_df = load_excerpts()

merged_df = excerpts_df.merge(
    contracts_df,
    on="contract_id",
    how="left",
    suffixes=("", "_contract"),
)

st.markdown("---")

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Contracts", f"{contracts_df['contract_id'].nunique():,}")
metric_2.metric("Excerpts", f"{excerpts_df['excerpt_id'].nunique():,}")
metric_3.metric("Contract Types", f"{contracts_df['contract_type'].nunique():,}")
metric_4.metric("Clause Categories", f"{excerpts_df['clause_category'].nunique():,}")

st.markdown("---")
st.markdown("### Filters")

f1, f2, f3, f4 = st.columns(4)

contract_type_options = ["All"] + sorted(
    [v for v in merged_df["contract_type"].dropna().astype(str).unique().tolist()]
)
clause_category_options = ["All"] + sorted(
    [v for v in merged_df["clause_category"].dropna().astype(str).unique().tolist()]
)
difficulty_options = ["All"] + sorted(
    [v for v in merged_df["difficulty_level"].dropna().astype(str).unique().tolist()]
)
trick_type_options = ["All"] + sorted(
    [v for v in merged_df["trick_type"].dropna().astype(str).unique().tolist()]
)

selected_contract_type = f1.selectbox("Contract Type", contract_type_options)
selected_clause_category = f2.selectbox("Clause Category", clause_category_options)
selected_difficulty = f3.selectbox("Difficulty Level", difficulty_options)
selected_trick_type = f4.selectbox("Trick Type", trick_type_options)

filtered_df = merged_df.copy()

if selected_contract_type != "All":
    filtered_df = filtered_df[filtered_df["contract_type"] == selected_contract_type]
if selected_clause_category != "All":
    filtered_df = filtered_df[filtered_df["clause_category"] == selected_clause_category]
if selected_difficulty != "All":
    filtered_df = filtered_df[filtered_df["difficulty_level"] == selected_difficulty]
if selected_trick_type != "All":
    filtered_df = filtered_df[filtered_df["trick_type"] == selected_trick_type]

st.markdown("---")
st.markdown("### Joined Dataset View")
st.caption("Excerpts are joined to contracts using `contract_id`.")

view_columns = [
    "excerpt_id",
    "contract_id",
    "contract_type",
    "counterparty",
    "clause_category",
    "difficulty_level",
    "trick_type",
    "industry",
    "agreement_date",
]

st.dataframe(
    filtered_df[view_columns].sort_values(["contract_type", "excerpt_id"]),
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")
st.markdown("### Excerpt Detail")

if filtered_df.empty:
    st.warning("No excerpts match the current filter set.")
else:
    excerpt_options = filtered_df["excerpt_id"].dropna().astype(str).unique().tolist()
    selected_excerpt_id = st.selectbox("Select an excerpt_id", excerpt_options)

    selected_row = filtered_df[filtered_df["excerpt_id"].astype(str) == selected_excerpt_id].iloc[0]

    top1, top2, top3, top4 = st.columns(4)
    top1.markdown(f"**Contract Type**  \n{selected_row['contract_type']}")
    top2.markdown(f"**Clause Category**  \n{selected_row['clause_category']}")
    top3.markdown(f"**Difficulty**  \n{selected_row['difficulty_level']}")
    top4.markdown(f"**Trick Type**  \n{selected_row['trick_type']}")

    with st.container(border=True):
        st.markdown("**Full Excerpt Text**")
        st.write(selected_row["excerpt_text"])
