from pathlib import Path


def test_required_skeleton_paths_exist() -> None:
    required = [
        "app.py",
        "requirements.txt",
        "README.md",
        "data",
        "docs",
        "pages",
        "utils",
        "scripts",
        "tests",
    ]
    for item in required:
        assert Path(item).exists()
