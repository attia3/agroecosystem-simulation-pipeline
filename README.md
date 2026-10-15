# Agroecosystem Simulation Pipeline

**Spatial modeling • Climate and soil data • Carbon dynamics • Reproducible analysis**

Research-driven workflows for preparing environmental forcing data, running regional agroecosystem scenarios, analyzing SOC–N₂O responses, and documenting calculations. The architecture is **model-agnostic**, with historical DSSAT integrations retained as an example backend.

**Project status:** Peer-reviewed research code and tested reusable utilities; **not** a fully validated operational MRV/credit issuance platform.

## From environmental data to model outputs

```text
Gridded climate + soil profiles + management + locations
              │
  Climate harmonization and input validation
              │
     Scenario orchestration and model runs
              │
  SOC, N₂O, yield and water-related outputs
              │
  Spatial post-processing, sensitivity checks,
  uncertainty assessment and decision support
```

## What is implemented

| Area | Available code | Status |
| --- | --- | --- |
| Climate preprocessing | `src/agroecosystem_pipeline/climate.py` | New unit-aware functions; local unit tests passed |
| Independent model evaluation | `src/agroecosystem_pipeline/evaluation.py` | Mean error, MAE, RMSE, empirical interval coverage and leave-one-group-out splits |
| Model execution / provenance | `src/agroecosystem_pipeline/execution.py` | New dry-run-safe runner, file hashes and JSON run records; local unit tests passed |
| NetCDF handling | `Process_netCDF.py` | Historical DSSAT-specific research script, not portable as-is |
| Weather files | `dssat_wthfunction.py` | Historical model-format writer requiring input validation |
| Regional scenario loops | `Run_dssat_T_Github.py` | Historical driver with absolute paths, licensed data dependencies |
| Output processing | `readDssatSummary.py` | Historical `Summary.OUT` reader requiring more format tests |
| Emission accounting | `N2Ofunction.py` | Research utility; assumptions must be matched to use case |

### Quick start — tested reusable utilities

Requires Python 3.10+.

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

```python
from agroecosystem_pipeline.climate import (
    convert_climate_units, relative_humidity_from_specific_humidity
)
from agroecosystem_pipeline.execution import execute_model

rain_mm_day = convert_climate_units(0.0001, "pr", "kg m-2 s-1")
relative_humidity = relative_humidity_from_specific_humidity(0.01, 25.0)
# Defaults to dry-run; substitute your installed model command and work dir:
# run = execute_model(["/path/to/model", "scenario.txt"], cwd="/data/experiment")
```

The new utilities have 15 local unit tests; GitHub CI should independently verify the pull request. Full model integrations still require licensed simulation software. **full model integrations require a licensed installation, real experiment inputs and separate validation**. An archived script is not considered a tested replacement for a published scientific workflow.

## Scientific evidence and repositories

- **Texas High Plains rotations:** Attia et al. (2025), *Unlocking climate resilience by exploring the mitigation potential of improved rotation with cover cropping*. **Journal of Environmental Management**, 391, 126352. https://doi.org/10.1016/j.jenvman.2025.126352
- **Surrogate modeling of SOC/N₂O responses:** [THP-SOC-N2O-ML-surrogate](https://github.com/attia3/THP-SOC-N2O-ML-surrogate) | https://doi.org/10.3390/agronomy16171679
- **Spatial disaggregation and validation:** [NAYD](https://github.com/attia3/nayd) | https://doi.org/10.3390/su18146937
- **Soil carbon sensitivity and calibration:** [DSSATcorncalibration](https://github.com/attia3/DSSATcorncalibration) (legacy URL; name change proposed).

The paper provides evidence for the scientific findings; the current public files should not be assumed to reproduce every published figure without external experiment inputs.

## Model adaptability

The climate conversions, subprocess orchestrator and run manifest do not depend on a specific biogeochemical model. Model-specific input exporters, parsers, and scientific parameter mappings must be implemented and independently checked for each engine (e.g., DSSAT, DayCent, RothC, APSIM). **No adapters for those other engines are claimed to be implemented.**

## Review and development

- [Code/source inventory](docs/UPLOADED_SOURCE_INVENTORY.md)
- [Refactoring, QA and reproducibility roadmap](docs/ROADMAP.md)
- [Pull request containing modernization changes](https://github.com/attia3/dssat-py-batchrunner/pull/1)

Publication, regulatory verification and operational carbon-crediting remain separate validation processes. This repository is **not** an approved carbon-credit quantification methodology or verifier-certified system.

## Citation and rights

Ahmed Attia. Please cite the relevant peer-reviewed paper for scientific findings and record the specific commit when referencing code. DSSAT executables and any proprietary or institutional inputs are not distributed. No open-source license has been chosen yet; do not assume a particular reuse license.
