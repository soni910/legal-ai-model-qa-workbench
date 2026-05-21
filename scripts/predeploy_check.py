"""Basic predeploy checks for project skeleton completeness."""

from pathlib import Path


REQUIRED_PATHS = [
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


def main() -> None:
    missing = [path for path in REQUIRED_PATHS if not Path(path).exists()]
    if missing:
        raise SystemExit(f"Missing required paths: {missing}")
    print("Predeploy check passed for skeleton structure.")


if __name__ == "__main__":
    main()
