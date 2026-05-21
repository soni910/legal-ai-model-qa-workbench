import streamlit as st

from utils.data_loader import load_model_runs, load_prompt_versions

st.set_page_config(page_title="Prompt & Model Runs", layout="wide")

st.title("🧪 Prompt & Model Runs")
st.caption(
    "Compare prompt iterations, track run history, and understand why versioned instruction design improves legal AI QA reliability."
)

hero_left, hero_right = st.columns([1.5, 1])
with hero_left:
    st.markdown(
        """
### Why prompt versioning matters
Small wording changes in extraction instructions can materially impact:
- clause-scope precision
- exception handling
- source-text grounding quality
- escalation behavior on ambiguous legal language

Versioning prompts creates **traceability** from instruction design to observed quality outcomes.
        """
    )
with hero_right:
    st.info(
        "**Portfolio context**\n\n"
        "All model outputs shown in this project are **simulated synthetic QA artifacts** "
        "created for demonstration purposes."
    )

prompt_df = load_prompt_versions()
runs_df = load_model_runs()

st.markdown("---")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Prompt Versions", f"{prompt_df['prompt_version'].nunique():,}")
kpi2.metric("Model Runs", f"{runs_df['run_id'].nunique():,}")
kpi3.metric("Models", f"{runs_df['model_name'].nunique():,}")
kpi4.metric("Reviewers", f"{runs_df['reviewer'].nunique():,}")

st.markdown("---")
st.subheader("Prompt Version Library")
st.caption("Each prompt card includes objective, known trade-offs, and full instruction text.")

for _, row in prompt_df.sort_values("prompt_version").iterrows():
    with st.container(border=True):
        header_left, header_right = st.columns([2, 1])
        with header_left:
            st.markdown(f"### {row['prompt_version']} · {row['prompt_name']}")
        with header_right:
            run_count = int((runs_df["prompt_version"] == row["prompt_version"]).sum())
            st.metric("Linked Runs", run_count)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Intended Improvement**")
            st.success(str(row["intended_improvement"]))
        with c2:
            st.markdown("**Known Limitations**")
            st.warning(str(row["known_limitations"]))

        st.markdown("**Prompt Text**")
        st.code(str(row["prompt_text"]), language="text")

st.markdown("---")
st.subheader("Model Runs Linked to Prompt Versions")
st.caption("Run metadata is joined to prompt metadata via `prompt_version`.")

linked_df = runs_df.merge(
    prompt_df[["prompt_version", "prompt_name", "intended_improvement", "known_limitations"]],
    on="prompt_version",
    how="left",
)

f1, f2, f3 = st.columns(3)
prompt_options = ["All"] + sorted(linked_df["prompt_version"].dropna().astype(str).unique().tolist())
model_options = ["All"] + sorted(linked_df["model_name"].dropna().astype(str).unique().tolist())
reviewer_options = ["All"] + sorted(linked_df["reviewer"].dropna().astype(str).unique().tolist())

selected_prompt = f1.selectbox("Filter by Prompt Version", prompt_options)
selected_model = f2.selectbox("Filter by Model", model_options)
selected_reviewer = f3.selectbox("Filter by Reviewer", reviewer_options)

filtered = linked_df.copy()
if selected_prompt != "All":
    filtered = filtered[filtered["prompt_version"] == selected_prompt]
if selected_model != "All":
    filtered = filtered[filtered["model_name"] == selected_model]
if selected_reviewer != "All":
    filtered = filtered[filtered["reviewer"] == selected_reviewer]

st.dataframe(
    filtered[
        [
            "run_id",
            "run_date",
            "model_name",
            "reviewer",
            "prompt_version",
            "prompt_name",
            "run_description",
            "intended_improvement",
            "known_limitations",
        ]
    ].sort_values(["run_date", "run_id"]),
    width="stretch",
    hide_index=True,
)

if filtered.empty:
    st.warning("No model runs match the current filter set.")
else:
    st.caption(f"Showing {len(filtered):,} linked run record(s).")
