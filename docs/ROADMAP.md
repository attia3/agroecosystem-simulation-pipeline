# Development roadmap — Agroecosystem Simulation Pipeline

This roadmap separates **model-specific existing research functionality** from improvements needed for a portable, maintainable workflow.

## Verified starting point

Five root-level Python scripts currently implement pieces of climate processing, DSSAT weather creation, run orchestration, summary parsing, and N₂O/GHG calculations. They are not currently organized as an installable package.

## Planned architecture (proposal, not existing files)

```text
src/dssat_spatial/
    climate.py            # NetCDF extraction, unit-aware harmonization
    weather.py            # DSSAT .WTH writer with strict validation
    experiments.py        # Experiment/rotation templates and batch files
    runner.py             # Configurable DSSAT CLI runner
    outputs.py            # Parser, metadata, provenance, aggregation
    ghg.py                # Transparent unit / factor accounting
configs/
    example.yaml          # Paths, scenarios, coordinates; no sensitive data
tests/
    test_climate.py       # Units, calendar, longitude edge cases
    test_weather.py       # Fixture-based .WTH formatting checks
    test_outputs.py       # Different output layouts and missing records
docs/
    reproducibility.md   # Environment, DSSAT version, run settings
```

## Priority order

1. **Inventory local scripts** and establish which scripts generated each publication figure/table.
2. **Protect reproducibility:** retain source snapshots under `legacy/` before refactoring.
3. **Externalize paths and inputs:** use configuration + environment variables; remove user home-drive locations and institution-specific paths.
4. **Validate climate inputs:** variable naming, Kelvin-to-Celsius conversion, precipitation rates/accumulations, missingness, lat/lon conventions, calendar/time indexing.
5. **Test DSSAT formatting and parsing:** known small fixtures; fail clearly on inconsistent dates or input columns.
6. **Add scenario/run provenance:** DSSAT version, code commit, input hashes, grid point, model/scenario/rotation ID, units, execution status.
7. **Handle results reproducibly:** structured outputs with stable naming, logging, and deterministic scenario runs.
8. **Set up CI:** lint/test checks that do not require DSSAT binaries; separate optional licensed-model integration tests.

## Current issues to investigate

- Main research driver contains absolute Windows paths and top-level execution.
- NetCDF processing functions rely on externally defined state in places.
- README previously referenced files not present in the public repository.
- Weather input handling and N₂O calculation assumptions require test fixtures.
- Public portfolio code must not be represented as a validated carbon-credit issuance pipeline.

**Publishing rule:** Only describe scripts as tested or reproducible after their dependencies and expected outputs have been verified.
