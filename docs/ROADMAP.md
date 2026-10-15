# Development roadmap — Agroecosystem Simulation Pipeline

This project separates **reusable model-independent utilities** from the **model-specific scripts retained as scientific provenance**.

## Current implemented functionality

- `src/agroecosystem_pipeline/climate.py` — unit-aware conversions, relative humidity and YYYYDDD calendar handling.
- `src/agroecosystem_pipeline/execution.py` — dry-run-safe external process execution, input hashing and JSON run records.
- `src/agroecosystem_pipeline/evaluation.py` — bias/accuracy/interval coverage metrics and leave-one-group-out splits.
- `tests/` — standard-library test suite; `.github/workflows/python-tests.yml` — CI definition.
- Root-level scripts — historical climate, DSSAT scenario execution, file parsing and GHG processing, not yet portable as-is.

## Outstanding work — verified science and engineering

1. **Secure the research baseline:** archive originals with commit identifiers and record which scripts generated each publication figure/table.
2. **Refactor model-specific adapters:** introduce explicit configuration and cleanly separated weather writers, model input generators and output parsers; no absolute local paths or implicit working-directory state.
3. **Validate physical inputs:** distinguish precipitation flux from daily accumulated precipitation, test humidity/pressure assumptions, check coordinate conventions, leap calendars, time zones, missing values and units.
4. **Test model I/O:** fixture-based tests for the weather input file format, experiment/batch construction, output headers and negative/missing values.
5. **Expand provenance:** record model executable/version, experiment template, input data checksums, parameter settings, scenario gridpoint, timestamp and code revision.
6. **Independent scientific evaluation:** implement spatial/temporal blocking appropriate to the original study; prevent training/testing leakage; publish evaluation tables with clearly defined bias and interval coverage.
7. **Quantify uncertainty explicitly:** distinguish uncertainty in observations, scenario selection, parameters, model structure and area-weighted outputs; do not confuse predictive intervals with registry deductions.
8. **Document real reproducibility:** small permitted test fixtures, precise environment, dependencies, repository release and code-to-figure reproducibility map.
9. **Generalize through interfaces:** add adapters for other simulation engines only after their inputs, output variables and scientifically meaningful parameters are verified.

## Planned extensions (not present today)

```text
src/agroecosystem_pipeline/
    model_adapters/
        dssat.py
        other_engines/       # only after implementation and verification
    weather_writer.py
    experiment_builder.py
    output_parser.py
    spatial_aggregation.py
configs/
    example.yaml
examples/
    minimal_case/
tests/
    fixtures/
docs/
    reproducibility.md
```

## Important boundaries

- The original DSSAT scripts may overwrite model files and depend on licensed binaries/data. Work on isolated experiment copies.
- The model-independent utilities are only part of the research pipeline; integration with a scientific model must be separately tested.
- Neither the old scripts nor the new helpers are presented as an approved carbon-market MRV/issuance methodology.
