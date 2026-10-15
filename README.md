# DSSAT Spatial Simulation Pipeline

**Research workflow and reproducibility reference** for running DSSAT cropping-system simulations over multiple locations, climate scenarios, and crop rotations.

**Status:** Published research code / portfolio showcase; **not yet a turnkey, fully tested Python package**. The files currently demonstrate core processing stages but rely on local DSSAT installations, external datasets, and machine-specific paths. Work to make them configurable and testable is tracked in [the development roadmap](docs/ROADMAP.md).

## Why this project matters

The pipeline connects spatial soil and climate data to process-based simulations, then converts model outputs into structured regional analyses. It illustrates a practical path from heterogeneous scientific inputs to repeatable, documented computations. A future operational version would add configuration, systematic QA, tests, provenance, and validated uncertainty reporting.

### Processing stages

```text
Gridded climate / point locations / soils / management
    ↓  Extract and harmonize daily weather
DSSAT weather (.WTH) + scenario-specific inputs
    ↓  Generate batches and execute DSSAT
Model output (.OUT)
    ↓  Parse and organize simulation results
Site × rotation × scenario summaries and GHG indicators
```

## Code currently available

| File | Purpose | Current caveat |
| --- | --- | --- |
| `Process_netCDF.py` | Reads climate NetCDF, extracts location-based series, converts selected weather variables | Depends on external data-directory context; verify metadata, units and coordinate assumptions |
| `dssat_wthfunction.py` | Builds DSSAT weather files and includes annual CO₂ values | Requires prescribed input columns and thorough date/format validation |
| `Run_dssat_T_Github.py` | Research driver for point × climate-model × scenario DSSAT runs and output aggregation | Contains machine-specific paths and assumes locally available DSSAT and other functions/data |
| `readDssatSummary.py` | Parses DSSAT `Summary.OUT` and converts DSSAT dates | Needs tests covering different DSSAT formats and missing records |
| `N2Ofunction.py` | Research utility for specified N₂O / CO₂-equivalent computations | Assumptions and emissions factors require validation for each application |

**Important:** This table reflects the files actually present. Other filenames mentioned in older versions of this README were illustrative or local variants, not published modules.

## Research application

These methods support spatiotemporal simulation of crop rotations under baseline and future climates, and regional assessment of soil organic carbon (SOC), nitrous oxide (N₂O), and management trade-offs. Example scientific context:

- Attia et al. (2025). *Unlocking climate resilience by exploring the mitigation potential of improved rotation with cover cropping*. **Journal of Environmental Management**, 391, 126352. https://doi.org/10.1016/j.jenvman.2025.126352

The publication describes the scientific application. **This public repository does not include all inputs or guarantee complete reproduction of every reported result.** Please distinguish the code examples from a validated crediting/MRV workflow.

## Prerequisites and scope

- Python environment with scientific packages used by the specific script (e.g. pandas, NumPy, xarray, netCDF4, PyYAML).
- Separately installed/licensed DSSAT, with the correct version and executable path.
- DSSAT model files, valid soil/experiment inputs, management scenarios, CO₂ series, and appropriately licensed climate datasets.
- Adjust script configuration and local paths before use; do **not** run the main research driver unmodified on a new machine.

This code has not been certified against Verra VM0042, Isometric, or any other carbon-credit methodology. Any application to crediting needs independently reviewed monitoring protocols, statistical estimators, uncertainty accounting, and verification controls.

## Development priorities

See [docs/ROADMAP.md](docs/ROADMAP.md): isolate reusable functions; replace absolute paths with validated configuration; create unit and integration tests with synthetic fixtures; version DSSAT scenario configurations; check missing data and units; produce audit-traceable outputs.

## Related public repositories

- [NAYD R geospatial disaggregation](https://github.com/attia3/nayd) — a reproducible spatial-data processing example.
- [SOC–N₂O ML surrogate](https://github.com/attia3/THP-SOC-N2O-ML-surrogate) — emulator of DSSAT-modeled management responses.

## Author and citation

Ahmed Attia. For published scientific findings, cite the associated peer-reviewed article; for code, reference the repository and the specific Git commit. Licensing terms for third-party DSSAT inputs, executables, and climate data apply separately.

## License

No open-source license is currently specified. Do not presume reuse rights until an explicit license is added.
