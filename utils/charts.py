"""Chart helpers for Streamlit/Altair visualizations."""

import altair as alt
import pandas as pd


def empty_bar_chart() -> alt.Chart:
    """Return a minimal empty chart placeholder."""
    frame = pd.DataFrame({"category": [], "value": []})
    return alt.Chart(frame).mark_bar().encode(x="category:N", y="value:Q")
