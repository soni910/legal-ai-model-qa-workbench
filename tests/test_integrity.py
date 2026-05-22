import pandas as pd

from utils.data_loader import (
    load_contracts,
    load_excerpts,
    load_gold_labels,
    load_model_outputs,
)


def test_all_output_label_ids_exist_in_gold_labels() -> None:
    outputs_df = load_model_outputs()
    labels_df = load_gold_labels()

    output_label_ids = set(outputs_df["label_id"].astype(str).tolist())
    gold_label_ids = set(labels_df["label_id"].astype(str).tolist())

    missing = output_label_ids - gold_label_ids
    assert not missing, f"Missing label_id references in gold_labels.csv: {sorted(missing)}"


def test_all_label_excerpt_ids_exist_in_excerpts() -> None:
    labels_df = load_gold_labels()
    excerpts_df = load_excerpts()

    label_excerpt_ids = set(labels_df["excerpt_id"].astype(str).tolist())
    excerpt_ids = set(excerpts_df["excerpt_id"].astype(str).tolist())

    missing = label_excerpt_ids - excerpt_ids
    assert not missing, f"Missing excerpt_id references in excerpts.csv: {sorted(missing)}"


def test_contract_id_relationships_are_consistent_across_files() -> None:
    contracts_df = load_contracts()
    excerpts_df = load_excerpts()
    labels_df = load_gold_labels()
    outputs_df = load_model_outputs()

    valid_contract_ids = set(contracts_df["contract_id"].astype(str).tolist())

    excerpt_contract_ids = set(excerpts_df["contract_id"].astype(str).tolist())
    label_contract_ids = set(labels_df["contract_id"].astype(str).tolist())
    output_contract_ids = set(outputs_df["contract_id"].astype(str).tolist())

    missing_in_excerpts = excerpt_contract_ids - valid_contract_ids
    missing_in_labels = label_contract_ids - valid_contract_ids
    missing_in_outputs = output_contract_ids - valid_contract_ids

    assert not missing_in_excerpts, (
        f"Invalid contract_id values in excerpts.csv: {sorted(missing_in_excerpts)}"
    )
    assert not missing_in_labels, (
        f"Invalid contract_id values in gold_labels.csv: {sorted(missing_in_labels)}"
    )
    assert not missing_in_outputs, (
        f"Invalid contract_id values in model_outputs.csv: {sorted(missing_in_outputs)}"
    )

    # Row-level consistency checks across joins
    label_join = labels_df[["label_id", "contract_id", "excerpt_id"]].merge(
        excerpts_df[["excerpt_id", "contract_id"]],
        on="excerpt_id",
        how="left",
        suffixes=("_label", "_excerpt"),
    )
    inconsistent_label_contract = label_join[
        label_join["contract_id_label"].astype(str) != label_join["contract_id_excerpt"].astype(str)
    ]
    assert inconsistent_label_contract.empty, "contract_id mismatch between gold_labels and excerpts"

    output_join = outputs_df[["output_id", "label_id", "contract_id", "excerpt_id"]].merge(
        labels_df[["label_id", "contract_id", "excerpt_id"]],
        on="label_id",
        how="left",
        suffixes=("_output", "_label"),
    )
    inconsistent_output_contract = output_join[
        output_join["contract_id_output"].astype(str)
        != output_join["contract_id_label"].astype(str)
    ]
    inconsistent_output_excerpt = output_join[
        output_join["excerpt_id_output"].astype(str) != output_join["excerpt_id_label"].astype(str)
    ]

    assert inconsistent_output_contract.empty, "contract_id mismatch between model_outputs and gold_labels"
    assert inconsistent_output_excerpt.empty, "excerpt_id mismatch between model_outputs and gold_labels"
