# Makefile — Causal Pollution-Health Brazil
# ==========================================
#
# Reproducible pipeline for estimating heterogeneous causal effects
# of air pollution on respiratory hospitalizations across 27 Brazilian
# state capitals.
#
# Usage:
#   make all         # Run full pipeline (extract -> process -> analyze -> figures)
#   make extract     # Download data from Supabase
#   make process     # Build the analysis panel
#   make analyze     # Run all causal models + sensitivity
#   make figures     # Generate all publication figures
#   make clean       # Remove generated outputs (keeps raw data)
#   make cleanall    # Remove everything including raw data

SHELL := /bin/bash
PYTHON := .venv/bin/python

# Parquet files produced by extraction
RAW_DATA := data/raw/weather_history.parquet \
            data/raw/air_quality_history.parquet \
            data/raw/health_hospitalizations.parquet \
            data/raw/demographics_history.parquet \
            data/raw/fleet_history.parquet

PANEL := data/processed/analysis_panel.parquet

# ---------------------------------------------------------------------------
# Phony targets
# ---------------------------------------------------------------------------
.PHONY: all extract process analyze figures clean cleanall venv

all: extract process analyze figures

# ---------------------------------------------------------------------------
# Virtual environment
# ---------------------------------------------------------------------------
venv: .venv/bin/activate

.venv/bin/activate:
	python3 -m venv .venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install pandas numpy scipy statsmodels econml shap \
		xgboost lightgbm matplotlib seaborn geopandas requests pyarrow

# ---------------------------------------------------------------------------
# Stage 1: Data extraction from Supabase
# ---------------------------------------------------------------------------
extract: venv $(RAW_DATA)

$(RAW_DATA): src/data/extract.py src/utils/config.py
	$(PYTHON) src/data/extract.py

# ---------------------------------------------------------------------------
# Stage 2: Data processing
# ---------------------------------------------------------------------------
process: extract $(PANEL)

$(PANEL): src/data/process.py src/utils/config.py $(RAW_DATA)
	$(PYTHON) src/data/process.py

# ---------------------------------------------------------------------------
# Stage 3: Analysis (models + diagnostics)
# ---------------------------------------------------------------------------
analyze: process
	$(PYTHON) src/models/causal_forest.py
	$(PYTHON) src/models/dml.py
	$(PYTHON) src/analysis/shap_analysis.py
	$(PYTHON) src/analysis/policy.py
	$(PYTHON) src/analysis/sensitivity.py

# ---------------------------------------------------------------------------
# Stage 4: Figures and tables
# ---------------------------------------------------------------------------
figures: analyze
	$(PYTHON) src/visualization/maps.py
	$(PYTHON) src/visualization/forest_plots.py
	$(PYTHON) src/visualization/shap_plots.py
	$(PYTHON) src/visualization/policy_plots.py

# ---------------------------------------------------------------------------
# Clean targets
# ---------------------------------------------------------------------------
clean:
	rm -rf data/interim/*
	rm -rf data/processed/*
	rm -rf outputs/figures/*
	rm -rf outputs/tables/*
	rm -rf outputs/reports/*
	rm -rf outputs/models/*
	@echo "Cleaned generated outputs (raw data preserved)."

cleanall: clean
	rm -rf data/raw/*.parquet
	rm -rf data/raw/shapefiles/
	@echo "Cleaned everything including raw data."
