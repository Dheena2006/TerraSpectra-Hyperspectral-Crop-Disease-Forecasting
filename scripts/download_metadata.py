"""Download only small annotation files from the official Dataverse dataset.

This deliberately avoids downloading the multi-GB hyperspectral image archives.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import requests

PERSISTENT_ID = "doi:10.57745/WVP0FJ"
API_BASE = "https://entrepot.recherche.data.gouv.fr/api"
TARGET_FILES = {"Data_description.csv", "VNIR_data.csv", "SWIR_data.csv"}
OUTPUT_DIR = Path("data/metadata")
TIMEOUT = (20, 180)


def get_latest_version(session: requests.Session) -> dict[str, Any]:
    url = f"{API_BASE}/datasets/:persistentId/"
    response = session.get(url, params={"persistentId": PERSISTENT_ID}, timeout=TIMEOUT)
    response.raise_for_status()
    payload = response.json()
    if payload.get("status") != "OK":
        raise RuntimeError(f"Dataverse API returned unexpected status: {payload.get('status')}")
    return payload["data"]["latestVersion"]


def flatten_files(version: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for item in version.get("files", []):
        data_file = item.get("dataFile", {})
        records.append({
            "id": data_file.get("id"),
            "filename": data_file.get("filename") or item.get("label"),
            "label": item.get("label"),
            "directoryLabel": item.get("directoryLabel"),
            "filesize": data_file.get("filesize"),
            "contentType": data_file.get("contentType"),
            "checksum": data_file.get("md5"),
        })
    return records


def download_file(session: requests.Session, file_id: int, destination: Path) -> None:
    url = f"{API_BASE}/access/datafile/{file_id}"
    with session.get(url, stream=True, timeout=TIMEOUT) as response:
        response.raise_for_status()
        with destination.open("wb") as output:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    output.write(chunk)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with requests.Session() as session:
        version = get_latest_version(session)
        inventory = flatten_files(version)
        (OUTPUT_DIR / "dataset_inventory.json").write_text(
            json.dumps({"persistent_id": PERSISTENT_ID, "files": inventory}, indent=2),
            encoding="utf-8",
        )

        by_name = {Path(str(item["filename"])).name: item for item in inventory}
        missing = sorted(TARGET_FILES - set(by_name))
        if missing:
            available = sorted(by_name)
            raise FileNotFoundError(
                f"Expected metadata files not found: {missing}. "
                f"Available file names in latest version: {available}"
            )

        for filename in sorted(TARGET_FILES):
            item = by_name[filename]
            file_id = item.get("id")
            if not file_id:
                raise ValueError(f"No Dataverse file ID found for {filename}")
            destination = OUTPUT_DIR / filename
            if destination.exists() and destination.stat().st_size > 0:
                print(f"Already present; skipping: {destination}")
                continue
            print(f"Downloading {filename} (Dataverse file ID {file_id})")
            download_file(session, int(file_id), destination)
            print(f"Saved {destination} ({destination.stat().st_size:,} bytes)")

    print("Metadata acquisition complete. No hyperspectral image archives were downloaded.")


if __name__ == "__main__":
    main()
