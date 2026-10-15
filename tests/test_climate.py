"""Unit tests run without licensed modeling software."""
import sys
import unittest
from datetime import date
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from agroecosystem_pipeline.climate import (
    ClimateInputError, convert_climate_units, parse_year_doy,
    relative_humidity_from_specific_humidity, year_doy,
)


class ClimateTests(unittest.TestCase):
    def test_radiation(self):
        self.assertAlmostEqual(convert_climate_units(200, "rsds", "W/m2").item(), 17.28)
    def test_temperature(self):
        self.assertAlmostEqual(convert_climate_units(300, "tasmax", "K").item(), 26.85)
    def test_precipitation_units(self):
        self.assertAlmostEqual(convert_climate_units(0.0001, "pr", "kg m-2 s-1").item(), 8.64)
        self.assertAlmostEqual(convert_climate_units(8.64, "pr", "mm/day").item(), 8.64)
    def test_invalid_units(self):
        with self.assertRaises(ClimateInputError):
            convert_climate_units(1, "pr", "unknown")
    def test_negative_precip(self):
        with self.assertRaises(ClimateInputError):
            convert_climate_units(-1, "pr", "mm/day")
    def test_rh(self):
        rh = relative_humidity_from_specific_humidity(0.01, 25, 1013.25).item()
        self.assertTrue(0 < rh <= 100)
    def test_calendar(self):
        for d in (date(2024, 2, 29), date(2025, 12, 31)):
            self.assertEqual(parse_year_doy(year_doy(d)), d)
    def test_invalid_doy(self):
        with self.assertRaises(ClimateInputError):
            parse_year_doy("2025366")


if __name__ == "__main__":
    unittest.main()
