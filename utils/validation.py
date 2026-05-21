"""Validation helpers for dataset schemas and required columns."""


def validate_required_columns(columns: list[str], required: list[str]) -> list[str]:
    """Return missing required columns."""
    return [name for name in required if name not in columns]
