# Research scripts reviewed from supplied Python archive

The supplied `Python Scripts.zip` includes 29 Python scripts, primarily encompassing simulation drivers, gridded climate processing, model output parsing, soil-profile extraction, and the SOC–N₂O ML surrogate analysis.

## Relevant source groups

- **Climate preprocessing:** `Process_netCDF.py`, `dssat_wthfunction.py` — gridded climate input, unit conversions, weather files and annual CO₂ forcing.
- **Regional simulations:** `Run_dssat_T_Github.py`, `Run_dssat_T_modified.py`, `Run_dssat_T_modified_RCP45.py`, `Run_dssat_T_modified_RCP85.py` — regional scenarios, model orchestration and outputs.
- **Model output readers:** `readDssatSummary.py`, `read_dssat_Arno_workingV.py`, `Simple_fun_Read_dssat.py` — structured extraction from text-based simulation outputs.
- **SOC/N₂O surrogate modeling:** `00_extract_soil_properties_from_US_SOL.py`, `01_build_ml_datasets.py`, `02_train_bau_relative_models.py`, `03_train_cover_crop_added_effect_models.py`, `06_model_performance_importance_SHAP.py` and related mapping scripts.
- **Other files:** research plotting tools, exercises, CSV outputs, exploratory notebooks and Python bytecode were not bulk-imported.

## New reusable components

- `src/agroecosystem_pipeline/climate.py` refactors climate unit conversion and humidity calculations into unit-aware, testable, model-agnostic functions.
- `src/agroecosystem_pipeline/execution.py` adds dry-run-safe simulation launching, input hashing, and JSON run records. It does not execute a model unless explicitly enabled.
- `tests/` covers the new functions without requiring licensed model software.

## Integrity and publication limits

The archive includes multiple variants of drivers with hard-coded home/workplace file paths, top-level execution, output-file mutation, and dependencies on licensed model installations or institution-specific climate/soil files. Publishing all scripts verbatim would imply unsupported portability and potentially disclose local paths or data. The original research scripts remain **available in the existing repository or the local archive**, rather than being silently relabeled as production modules.

Scientific results must be validated against the referenced publications before describing any rewritten module as a numerically equivalent replacement. The new code is infrastructure: it is **not** a validated Verra/Isometric MRV or carbon-crediting engine.
