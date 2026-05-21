from utils.data_loader import load_all_data
from utils.validation import REQUIRED_COLUMNS, validate_all_datasets, validate_columns


def test_validate_columns_required_columns_exist() -> None:
    datasets = load_all_data()
    for name, frame in datasets.items():
        is_valid, message = validate_columns(name, frame.columns.tolist())
        assert is_valid
        assert "all required columns" in message


def test_validate_all_datasets_reports_pass() -> None:
    results = validate_all_datasets()
    assert set(results.keys()) == set(REQUIRED_COLUMNS.keys())
    for message in results.values():
        assert message.startswith("PASS:")
