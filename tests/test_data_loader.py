from utils.data_loader import (
    load_all_data,
    load_contracts,
    load_data_dictionary,
    load_error_taxonomy,
    load_excerpts,
    load_gold_labels,
    load_model_outputs,
    load_model_runs,
    load_prompt_versions,
)


def test_each_csv_loads_and_is_non_empty() -> None:
    datasets = [
        load_contracts(),
        load_excerpts(),
        load_gold_labels(),
        load_prompt_versions(),
        load_model_runs(),
        load_model_outputs(),
        load_error_taxonomy(),
        load_data_dictionary(),
    ]
    for frame in datasets:
        assert not frame.empty


def test_load_all_data_returns_all_expected_datasets() -> None:
    expected = {
        "contracts",
        "excerpts",
        "gold_labels",
        "prompt_versions",
        "model_runs",
        "model_outputs",
        "error_taxonomy",
        "data_dictionary",
    }
    loaded = load_all_data()
    assert set(loaded.keys()) == expected
    for frame in loaded.values():
        assert not frame.empty
