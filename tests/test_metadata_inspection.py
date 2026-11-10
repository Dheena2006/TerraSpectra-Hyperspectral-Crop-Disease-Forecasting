from scripts.download_metadata import flatten_files
from scripts.inspect_metadata import summarize_csv


def test_flatten_files_extracts_dataverse_file_fields():
    version = {
        "files": [{
            "label": "VNIR_data.csv",
            "directoryLabel": "Data annotation",
            "dataFile": {
                "id": 123,
                "filename": "VNIR_data.csv",
                "filesize": 5600,
                "contentType": "text/csv",
                "md5": "abc",
            },
        }]
    }
    result = flatten_files(version)
    assert result[0]["id"] == 123
    assert result[0]["filename"] == "VNIR_data.csv"
    assert result[0]["directoryLabel"] == "Data annotation"


def test_summarize_csv_reports_shape_and_columns(tmp_path):
    import pandas as pd

    csv_path = tmp_path / "sample.csv"
    pd.DataFrame({"label": ["healthy", "infected"], "day": [0, 3]}).to_csv(csv_path, index=False)
    result = summarize_csv(csv_path)
    assert result["rows"] == 2
    assert result["columns"] == 2
    assert result["column_names"] == ["label", "day"]
