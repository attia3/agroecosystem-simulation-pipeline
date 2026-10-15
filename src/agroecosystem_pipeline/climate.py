"""Unit-aware weather preprocessing extracted from regional modeling methods.

This module is model-agnostic. Weather forcing metadata and simulation units
must be independently validated before scientific or crediting use.
"""
from __future__ import annotations
from datetime import date, timedelta
from typing import Any
import numpy as np


class ClimateInputError(ValueError):
    """Input units, dates or physical ranges are invalid."""


def convert_climate_units(values: Any, variable: str, units: str) -> np.ndarray:
    """Return C, MJ m-2 day-1, mm day-1, or kg/kg from explicit input units."""
    x = np.asarray(values, dtype=float)
    var = variable.strip().lower()
    u = units.strip().lower().replace(" ", "")
    if var in {"tasmax", "tasmin", "temperature"}:
        if u in {"k", "kelvin"}:
            out = x - 273.15
        elif u in {"c", "degc", "celsius", "degree_celsius"}:
            out = x
        else:
            raise ClimateInputError(f"Unsupported temperature units: {units}")
    elif var in {"rsds", "srad", "radiation"}:
        if u in {"w/m2", "wm-2", "wm^-2"}:
            out = x * 0.0864
        elif u in {"mj/m2/day", "mjm-2day-1", "mjm^-2day^-1"}:
            out = x
        else:
            raise ClimateInputError(f"Unsupported radiation units: {units}")
    elif var in {"pr", "rain", "precipitation"}:
        if u in {"kg/m2/s", "kgm-2s-1", "kgm^-2s^-1", "mm/s"}:
            out = x * 86400.0
        elif u in {"mm/day", "mmd-1", "mmd^-1", "mm"}:
            out = x
        else:
            raise ClimateInputError(f"Unsupported precipitation units: {units}")
        if np.any(np.isfinite(out) & (out < 0)):
            raise ClimateInputError("Negative precipitation requires input review")
    elif var in {"huss", "specific_humidity"}:
        if u not in {"1", "kg/kg", "kgkg-1"}:
            raise ClimateInputError(f"Unsupported humidity units: {units}")
        out = x
        if np.any(np.isfinite(out) & ((out < 0) | (out >= 1))):
            raise ClimateInputError("Specific humidity must lie in [0, 1)")
    else:
        raise ClimateInputError(f"Unsupported variable: {variable}")
    return np.asarray(out, dtype=float)


def relative_humidity_from_specific_humidity(
    specific_humidity: Any,
    temperature_c: Any,
    pressure_hpa: Any = 1013.25,
) -> np.ndarray:
    """Calculate RH (%) from q, Celsius temperature, and pressure in hPa.

    Standard-pressure default is a simplifying assumption: use site pressure
    where available. Supersaturation values are clipped after conversion.
    """
    q, t, p = np.broadcast_arrays(
        np.asarray(specific_humidity, dtype=float),
        np.asarray(temperature_c, dtype=float),
        np.asarray(pressure_hpa, dtype=float),
    )
    if np.any(np.isfinite(q) & ((q < 0) | (q >= 1))):
        raise ClimateInputError("Specific humidity must lie in [0, 1)")
    if np.any(np.isfinite(p) & (p <= 0)):
        raise ClimateInputError("Pressure must be positive")
    es = 6.112 * np.exp(17.67 * t / (t + 243.5))
    e = q * p / (0.622 + 0.378 * q)
    return np.clip(100.0 * e / es, 0.0, 100.0)


def parse_year_doy(year_doy: int | str) -> date:
    """Parse 7-digit YYYYDDD, rejecting invalid leap-year day numbers."""
    token = str(year_doy).strip()
    if len(token) != 7 or not token.isdigit():
        raise ClimateInputError("Date must be YYYYDDD")
    year, day = int(token[:4]), int(token[4:])
    if not 1 <= year <= 9999:
        raise ClimateInputError("Invalid year")
    days = (date(year + 1, 1, 1) - date(year, 1, 1)).days if year < 9999 else 365
    if not 1 <= day <= days:
        raise ClimateInputError(f"Invalid day-of-year {day} for {year}")
    return date(year, 1, 1) + timedelta(days=day - 1)


def year_doy(value: date) -> int:
    """Return a YYYYDDD integer for a calendar date."""
    return value.year * 1000 + value.timetuple().tm_yday
