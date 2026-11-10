# TerraSpectra: Hyperspectral Crop Disease Forecasting

Research project for hyperspectral early detection of Septoria tritici blotch in durum wheat, with a separate investigation of temporal disease progression.

## Dataset

Primary source: [Early detection of septoria infection on wheat leaves using hyperspectral imaging data](https://doi.org/10.57745/WVP0FJ), Recherche Data Gouv, Lorraine Latchoumane (2024), Version 1.0.

The repository metadata describes healthy and *Zymoseptoria tritici*-infected durum wheat leaves, VNIR and SWIR acquisitions, 18 acquisition dates from one day before inoculation to 20 days after inoculation, and 1,175 images per spectral range covering 3,326 leaves. The dataset is distributed under Etalab Open License 2.0. Cite the dataset when using it.

**Research boundary:** these are controlled-condition experimental observations. They do not establish field-scale performance. Classification of current infection is not the same task as forecasting future disease. A forecasting claim requires identifiable repeated observations and future outcome labels, plus time-aware validation.

## Day 1 setup

### Google Colab
Open a new Colab notebook and clone the repository:

~~~python
!git clone https://github.com/Dheena2006/TerraSpectra-Hyperspectral-Crop-Disease-Forecasting.git
%cd TerraSpectra-Hyperspectral-Crop-Disease-Forecasting
!pip install -r requirements.txt
~~~

### Local computer
~~~bash
git clone https://github.com/Dheena2006/TerraSpectra-Hyperspectral-Crop-Disease-Forecasting.git
cd TerraSpectra-Hyperspectral-Crop-Disease-Forecasting
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
~~~

## Acquire the small annotation/metadata files first

~~~bash
python scripts/download_metadata.py
python scripts/inspect_metadata.py
~~~

The acquisition script uses the Dataverse API to resolve file IDs from the persistent dataset identifier. It downloads only the three small documentation CSVs (Data_description.csv, VNIR_data.csv, SWIR_data.csv) and a JSON dataset inventory. It does **not** download multi-gigabyte hyperspectral image archives.

Downloaded data and metadata are kept under data/ and excluded from Git. Inspect the inventory before choosing image archives.

## Repository layout

- scripts/download_metadata.py: resolve and download metadata from the official repository.
- scripts/inspect_metadata.py: report schema, missing values, and basic label/date information.
- notebooks/01_dataset_validation.ipynb: Colab-first Day 1 workflow.
- tests/: lightweight tests for metadata inspection utilities.

## Scientific safeguards

1. Keep observations from the same leaf/plant together when creating splits, if identifiers allow it.
2. Fit preprocessing and feature selection on training data only.
3. Do not infer temporal forecastability from a cross-sectional label table.
4. Record acquisition date, genotype, treatment, and sample identifiers where present.
5. Report macro-F1, per-class precision/recall, confusion matrix, and split strategy—not accuracy alone.

## Dataset citation

Latchoumane, L. (2024). *Early detection of septoria infection on wheat leaves using hyperspectral imaging data* (Version 1.0). Recherche Data Gouv. https://doi.org/10.57745/WVP0FJ

License: Etalab Open License 2.0. Check the dataset record for the authoritative terms and citation details.
