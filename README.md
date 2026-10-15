# Agroecosystem Simulation Pipeline

**Scalable process-based modeling · Spatial environmental data · SOC–N₂O analysis · Reproducible scientific workflows**

A research-oriented Python project for connecting **climate, soil, management, and geospatial inputs** to large-scale agroecosystem simulations and quantitative analysis. The reusable components are designed to be **model-independent**; the original research scripts demonstrate a **DSSAT-specific implementation**.

**Project scope:** research software and reusable analysis tools—not a certified carbon-crediting system or an out-of-the-box reproduction of every published result.

## Workflow

```text
Climate NetCDF + soil properties + management + locations
                         │
               Data harmonization & QA
                         │
               Model input preparation
                         │
             Scenario / batch simulation
                         │
       Output parsing and model evaluation
                         │
       Spatial summaries, SOC and N₂O analysis
                         │
           Reproducible research outputs
```

## Available code

### Reusable Python utilities

| Module | Capability |
| --- | --- |
| [`climate.py`](src/agroecosystem_pipeline/climate.py) | Unit-aware climate transformations, relative humidity, calendar checks |
| [`execution.py`](src/agroecosystem_pipeline/execution.py) | Configurable and dry-run-safe execution, SHA-256 file hashes, JSON run records |
| [`evaluation.py`](src/agroecosystem_pipeline/evaluation.py) | Bias, MAE, RMSE, prediction-interval coverage, leave-one-site/group-out splits |
| [`tests/`](tests/) | Unit tests for the reusable utilities, independent of DSSAT executables |

### Published research scripts retained for scientific provenance

| Script | Research purpose |
| --- | --- |
| [`Process_netCDF.py`](Process_netCDF.py) | Extracting and harmonizing gridded climate forcing for location-based simulations |
| [`dssat_wthfunction.py`](dssat_wthfunction.py) | Weather forcing generation with historical CO₂ series |
| [`Run_dssat_T_Github.py`](Run_dssat_T_Github.py) | Regional climate/rotation scenario orchestration and output aggregation |
| [`readDssatSummary.py`](readDssatSummary.py) | Parsing simulation summary outputs |
| [`N2Ofunction.py`](N2Ofunction.py) | Research-stage N₂O/emissions-accounting utilities |

**Important distinction:** The root-level scripts are historical research code; some contain absolute Windows paths and expect separately licensed model installations and project inputs. The new Python utilities do not yet replace the complete original simulation workflows.

## Installation and tests

Python 3.10+ is required for the reusable utilities.

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

A small, model-independent usage example:

```python
from agroecosystem_pipeline.climate import convert_climate_units
from agroecosystem_pipeline.evaluation import evaluate_predictions

rain_mm_day = convert_climate_units(0.0001, "pr", "kg m-2 s-1")
metrics = evaluate_predictions(
    observed=[20, 25, 30],
    predicted=[21, 23, 31],
)
print(rain_mm_day, metrics.rmse)
```

For explicit simulation execution and provenance recording, see [`execution.py`](src/agroecosystem_pipeline/execution.py). DSSAT binaries, experiment files, climate datasets, and institution-specific paths must be supplied and validated separately.

## Selected publications and related code

**Regional SOC and GHG analysis**

Attia, A., et al. (2025). [Unlocking climate resilience by exploring the mitigation potential of improved rotation with cover cropping](https://doi.org/10.1016/j.jenvman.2025.126352). *Journal of Environmental Management*, 391, 126352. This study provides scientific context for regional process-based simulations, cover-crop management, SOC stocks, and net GHG outcomes.

**Machine-learning model emulation**

[Machine-Learning Surrogate Modeling of SOC and N₂O Responses to Diversified Crop Rotations in the Texas High Plains](https://doi.org/10.3390/agronomy16171679) (*Agronomy*, 2026). Associated repository: [THP-SOC-N2O-ML-surrogate](https://github.com/attia3/THP-SOC-N2O-ML-surrogate).

**Spatial environmental analytics**

[Satellite-Guided Delineation of Crop Production Zones from Official Crop Statistics for Spatial Agricultural Decision Support](https://doi.org/10.3390/su18146937) (*Sustainability*, 2026). Associated R package: [NAYD](https://github.com/attia3/nayd).

**Sensitivity and model parameter evaluation**

See [Soil Carbon Sensitivity Analysis](https://github.com/attia3/soil-carbon-sensitivity-analysis), including maize calibration, co-inertia analysis, and Sobol variance decomposition.

The publications document scientific applications. Public code availability and numerical reproducibility may differ by study; not all licensed binaries, environmental datasets, or original model inputs are redistributed here.

## Why this architecture generalizes

Climate conversion, model execution, provenance recording, and predictive evaluation are independent of a particular process-based model. **Model-specific adapters remain necessary** for the input/output formats and parameter definitions of engines such as DSSAT, APSIM, DayCent, or RothC. Their implementation is future work, not an existing capability of this repository.

## Documentation

- [Research source inventory](docs/UPLOADED_SOURCE_INVENTORY.md)
- [Modernization and reproducibility roadmap](docs/ROADMAP.md)
- [Unit tests](tests/)

## Citation, limitations, and permissions

Maintained by **Ahmed Attia**. Cite the relevant peer-reviewed publication for scientific results and a **specific repository commit** for code. Model files and climate data may carry separate licensing or institutional restrictions.

**This repository is not a registry-approved SOC estimation, verification, or credit-issuance pipeline.** It should be independently evaluated before being adapted to operational MRV or high-stakes decisions.

An explicit open-source license has not yet been selected; do not assume reuse rights.
