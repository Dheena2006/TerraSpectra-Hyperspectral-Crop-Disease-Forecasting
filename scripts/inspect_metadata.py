"""Inspect downloaded CSV annotations without assuming their column schema."""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

DEFAULT_DIR = Path("data/metadata")


def summarize_csv(path: Path) -> dict[str, object]:
    frame = pd.read_csv(path)
    print(f"\n## {path.name}")
    print(f"Rows: {len(frame):,} | Columns: {len(frame.columns):,}")
    print("Columns and dtypes:")
    for column, dtype in frame.dtypes.items():
        print(f"  - {column}: {dtype}; missing={int(frame[column].isna().sum())}")
    print("\nPreview:")
    print(frame.head(5).to_string(index=False))
    return {
        "file": path.name,
        "rows": len(frame),
        "columns": len(frame.columns),
        "column_names": list(map(str, frame.columns)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata-dir", type=Path, default=DEFAULT_DIR)
    args = parser.parse_args()

    if not args.metadata_dir.exists():
        raise SystemExit(
            f"Metadata directory not found: {args.metadata_dir}. "
            "Run python scripts/download_metadata.py first."
        )

    files = sorted(
        path for path in args.metadata_dir.glob("*.csv")
        if path.name in {"Data_description.csv", "VNIR_data.csv", "SWIR_data.csv"}
    )
    if not files:
        raise SystemExit(f"No expected annotation CSVs found in {args.metadata_dir}")

    summaries = [summarize_csv(path) for path in files]
    print("\n## Inspection summary")
    for item in summaries:
        print(f"{item['file']}: {item['rows']} rows x {item['columns']} columns")


if __name__ == "__main__":
    main()
