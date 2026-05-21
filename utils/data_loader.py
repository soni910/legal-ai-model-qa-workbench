"""Data loading helpers for synthetic CSV inputs."""

from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load_csv(filename: str) -> pd.DataFrame:
    """Load a CSV file from the project data directory."""
    return pd.read_csv(DATA_DIR / filename)


def load_contracts() -> pd.DataFrame:
    return _load_csv("contracts.csv")


def load_excerpts() -> pd.DataFrame:
    return _load_csv("excerpts.csv")


def load_gold_labels() -> pd.DataFrame:
    return _load_csv("gold_labels.csv")


def load_prompt_versions() -> pd.DataFrame:
    return _load_csv("prompt_versions.csv")


def load_model_runs() -> pd.DataFrame:
    return _load_csv("model_runs.csv")


def load_model_outputs() -> pd.DataFrame:
    return _load_csv("model_outputs.csv")


def load_error_taxonomy() -> pd.DataFrame:
    return _load_csv("error_taxonomy.csv")


def load_data_dictionary() -> pd.DataFrame:
    return _load_csv("data_dictionary.csv")


def load_all_data() -> dict[str, pd.DataFrame]:
    """Load all project datasets keyed by filename stem."""
    return {
        "contracts": load_contracts(),
        "excerpts": load_excerpts(),
        "gold_labels": load_gold_labels(),
        "prompt_versions": load_prompt_versions(),
        "model_runs": load_model_runs(),
        "model_outputs": load_model_outputs(),
        "error_taxonomy": load_error_taxonomy(),
        "data_dictionary": load_data_dictionary(),
    }
