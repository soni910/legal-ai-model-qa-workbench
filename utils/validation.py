"""Validation helpers for dataset schemas and required columns."""

from utils.data_loader import load_all_data


REQUIRED_COLUMNS: dict[str, list[str]] = {
    "contracts": [
        "contract_id",
        "contract_type",
        "counterparty",
        "industry",
        "agreement_date",
        "synthetic_flag",
        "contract_summary",
    ],
    "excerpts": [
        "excerpt_id",
        "contract_id",
        "clause_category",
        "excerpt_text",
        "difficulty_level",
        "trick_type",
        "notes",
    ],
    "gold_labels": [
        "label_id",
        "excerpt_id",
        "contract_id",
        "field_name",
        "gold_answer",
        "gold_source_text",
        "answer_status",
        "requires_legal_sme",
        "ambiguity_flag",
        "label_notes",
    ],
    "prompt_versions": [
        "prompt_version",
        "prompt_name",
        "prompt_text",
        "intended_improvement",
        "known_limitations",
    ],
    "model_runs": [
        "run_id",
        "prompt_version",
        "model_name",
        "run_date",
        "run_description",
        "reviewer",
    ],
    "model_outputs": [
        "output_id",
        "run_id",
        "label_id",
        "excerpt_id",
        "contract_id",
        "field_name",
        "ai_answer",
        "ai_source_text",
        "confidence",
        "match_status",
        "score",
        "error_type",
        "severity",
        "source_match_status",
        "missed_nuance",
        "over_extracted",
        "escalation_required",
        "suggested_instruction_fix",
    ],
    "error_taxonomy": [
        "error_type",
        "definition",
        "example",
        "typical_severity",
        "escalation_guidance",
    ],
    "data_dictionary": [
        "file_name",
        "column_name",
        "meaning",
        "example_value",
        "required",
    ],
}


def validate_columns(dataset_name: str, columns: list[str]) -> tuple[bool, str]:
    """Validate required columns for one dataset with a clear message."""
    required = REQUIRED_COLUMNS.get(dataset_name)
    if required is None:
        return False, f"Unknown dataset '{dataset_name}'."

    missing = [column for column in required if column not in columns]
    if missing:
        return False, f"{dataset_name}: missing required columns: {', '.join(missing)}"
    return True, f"{dataset_name}: all required columns are present."


def validate_all_datasets() -> dict[str, str]:
    """Validate all loaded datasets and return clear status messages."""
    data = load_all_data()
    results: dict[str, str] = {}
    for dataset_name, frame in data.items():
        is_valid, message = validate_columns(dataset_name, frame.columns.tolist())
        prefix = "PASS" if is_valid else "FAIL"
        results[dataset_name] = f"{prefix}: {message}"
    return results
