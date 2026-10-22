"""Verificaciones locales de planificación e idempotencia simulada IGP."""

from pathlib import Path
import tempfile
import unittest

from openpyxl import Workbook

from igp.persistence_plan import (
    ACTION_INSERT,
    ACTION_INVALID,
    ACTION_SKIP,
    plan_rows,
    simulate_twice,
)
from igp.reader import SHEET_NAME, SOURCE_FIELDS


# =====================================================
# BLOQUE 1: Fixtures sintéticos, nunca datos oficiales.
# =====================================================
def fixture_row(**overrides):
    raw = dict(zip(SOURCE_FIELDS, (
        "2024-02-01", "12:01:02", -12.1, -77.0, 40, 4.5,
    )))
    raw.update(overrides)
    return raw


class PersistencePlanTests(unittest.TestCase):
    # =================================================
    # BLOQUE 2: Duplicado exacto y cambio de parámetro.
    # =================================================
    def test_repeat_same_batch_is_skipped(self):
        rows = [(2, fixture_row()), (3, fixture_row())]
        result = list(plan_rows(rows, file_digest="a" * 64))
        self.assertEqual(
            [record.action for record in result], [ACTION_INSERT, ACTION_SKIP]
        )
        self.assertEqual(result[0].fingerprint, result[1].fingerprint)
        self.assertEqual(result[1].staging_payload["excel_row"], 3)

    def test_second_batch_known_fingerprint_is_skipped(self):
        initial = list(plan_rows([(2, fixture_row())], file_digest="a" * 64))
        second = list(plan_rows(
            [(2, fixture_row())],
            file_digest="a" * 64,
            known_fingerprints={initial[0].fingerprint},
        ))
        self.assertEqual(second[0].action, ACTION_SKIP)

    def test_changed_parameter_is_new_candidate_not_auto_merge(self):
        first = list(plan_rows([(2, fixture_row())], file_digest="a" * 64))
        second = list(plan_rows(
            [(3, fixture_row(**{"profundidad (km)": 41}))],
            file_digest="a" * 64,
            known_fingerprints={first[0].fingerprint},
        ))
        self.assertEqual(second[0].action, ACTION_INSERT)
        self.assertNotEqual(first[0].fingerprint, second[0].fingerprint)

    def test_nearby_distinct_events_are_preserved(self):
        other = fixture_row(**{"hora UTC": "12:01:03"})
        result = list(plan_rows(
            [(2, fixture_row()), (3, other)], file_digest="a" * 64
        ))
        self.assertEqual([item.action for item in result], [ACTION_INSERT] * 2)

    # =================================================
    # BLOQUE 3: Registro inválido conservado para staging.
    # =================================================
    def test_invalid_row_is_kept_with_error(self):
        result = list(plan_rows(
            [(4, fixture_row(**{"latitud (º)": 999}))],
            file_digest="a" * 64,
        ))[0]
        self.assertEqual(result.action, ACTION_INVALID)
        self.assertIsNone(result.event)
        self.assertEqual(result.staging_payload["raw"]["latitud (º)"], 999)
        self.assertEqual(result.errors[0]["code"], "out_of_range")

    # =================================================
    # BLOQUE 4: Doble ejecución con XLSX local de prueba.
    # =================================================
    def test_two_pass_workbook_does_not_plan_second_insert(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "fixture.xlsx"
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = SHEET_NAME
            sheet.append(list(SOURCE_FIELDS))
            sheet.append(list(fixture_row().values()))
            sheet.append(list(fixture_row().values()))
            sheet.append(list(fixture_row(**{"latitud (º)": 999}).values()))
            workbook.save(path)
            report = simulate_twice(path)
            self.assertEqual(report["first_run"]["records_seen"], 3)
            self.assertEqual(report["first_run"]["insert_candidates"], 1)
            self.assertEqual(report["first_run"]["skip_exact_fingerprint"], 1)
            self.assertEqual(report["first_run"]["invalid_candidates"], 1)
            self.assertEqual(report["second_run"]["insert_candidates"], 0)
            self.assertEqual(report["second_run"]["skip_exact_fingerprint"], 2)
            self.assertEqual(report["second_run"]["invalid_candidates"], 1)
            self.assertFalse(report["database_writes"])


if __name__ == "__main__":
    unittest.main()
