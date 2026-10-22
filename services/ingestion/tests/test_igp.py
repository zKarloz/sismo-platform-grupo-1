"""Pruebas unitarias del contrato IGP y del dry-run local."""

import json
from pathlib import Path
import tempfile
import unittest

from openpyxl import Workbook

from igp.dry_run import run_dry_run
from igp.normalizer import normalize_igp_row
from igp.reader import SHEET_NAME, SOURCE_FIELDS


# =====================================================
# BLOQUE 1: Fixtures representativos sin datos ficticios
# presentados como eventos oficiales; solo son pruebas.
# =====================================================

def example_row(**changes):
    raw = dict(zip(SOURCE_FIELDS, (
        "2024-01-01", "07:06:07.00", -10.69, -78.54, 35, 4.2,
    )))
    raw.update(changes)
    return raw


class NormalizationTests(unittest.TestCase):
    # =================================================
    # BLOQUE 2: Formatos temporales, rangos e identidad.
    # =================================================

    def test_normalization_and_provenance(self):
        result = normalize_igp_row(example_row())
        self.assertEqual(result.errors, [])
        self.assertEqual(result.event["occurred_at"], "2024-01-01T07:06:07+00:00")
        self.assertEqual(result.event["depth_km"], 35.0)
        self.assertIsNone(result.event["external_id"])
        self.assertEqual(result.event["review_status"], "pending")
        self.assertEqual(len(result.fingerprint), 64)

    def test_repeat_is_deterministic(self):
        self.assertEqual(
            normalize_igp_row(example_row()).fingerprint,
            normalize_igp_row(example_row()).fingerprint,
        )

    def test_changed_parameter_has_new_record_fingerprint(self):
        self.assertNotEqual(
            normalize_igp_row(example_row()).fingerprint,
            normalize_igp_row(example_row(**{"profundidad (km)": 36})).fingerprint,
        )

    def test_non_finite_or_invalid_coordinates(self):
        for value in (None, "NaN", 95):
            with self.subTest(value=value):
                result = normalize_igp_row(example_row(**{"latitud (º)": value}))
                self.assertIsNone(result.event)
                self.assertTrue(result.errors)

    def test_invalid_timestamp(self):
        result = normalize_igp_row(example_row(**{"hora UTC": "25:70:10"}))
        self.assertEqual(result.errors[0]["code"], "invalid_datetime")

    def test_negative_depth_is_kept_for_review(self):
        result = normalize_igp_row(example_row(**{"profundidad (km)": -2}))
        self.assertTrue(any(e["code"] == "negative_depth" for e in result.errors))

    def test_decimal_format_consistency(self):
        a = normalize_igp_row(example_row(**{"magnitud (M)": 4.2}))
        b = normalize_igp_row(example_row(**{"magnitud (M)": "4.200"}))
        self.assertEqual(a.fingerprint, b.fingerprint)

    # =================================================
    # BLOQUE 3: Ensayar la ejecución completa sin BD.
    # =================================================

    def test_dry_run_reads_workbook_and_counts_errors(self):
        with tempfile.TemporaryDirectory() as temp:
            xlsx_path = Path(temp) / "igp_fixture.xlsx"
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = SHEET_NAME
            sheet.append(list(SOURCE_FIELDS))
            sheet.append(list(example_row().values()))
            sheet.append(list(example_row().values()))
            sheet.append(list(example_row(**{"latitud (º)": 999}).values()))
            workbook.save(xlsx_path)

            report = run_dry_run(xlsx_path)
            self.assertEqual(report["records_seen"], 3)
            self.assertEqual(report["records_valid"], 2)
            self.assertEqual(report["records_invalid"], 1)
            self.assertEqual(report["unique_record_fingerprints"], 1)
            self.assertEqual(report["repeated_record_fingerprints"], 1)
            self.assertEqual(report["events_by_year"], {"2024": 2})
            self.assertFalse(report["database_writes"])
            self.assertEqual(report["repeated_examples"][0]["first_excel_row"], 2)


if __name__ == "__main__":
    unittest.main()
