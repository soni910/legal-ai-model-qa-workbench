"""Data loading helpers for synthetic CSV inputs."""

from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")


def load_csv(filename: str) -> pd.DataFrame:
    """Load a CSV from the local data directory."""
    return pd.read_csv(DATA_DIR / filename)
