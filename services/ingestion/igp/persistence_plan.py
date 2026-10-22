"""Planificador de ingesta IGP sin base de datos ni escrituras externas.

Este módulo NO implementa persistencia real. Simula la decisión de
insertar/omitir/rechazar usando una identidad exacta (fingerprint v1).
"""

import argparse
from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
import json
import math
from pathlib import Path
from typing import Iterable, Iterator

from .dry_run import file_sha256
from .normalizer import normalize_igp_row
from .reader import iter_igp_rows

# =====================================================
# BLOQUE 1: Estados de planificación, sin SQL.
# Las decisiones no certifican duplicados físicos.
# =====================================================
ACTION_INSERT = "insert_candidate"
ACTION_SKIP = "skip_exact_fingerprint"
ACTION_INVALID = "invalid_to_staging"
FINGERPRINT_VERSION = "igp-record-v1"


@dataclass(frozen=True)
class PlannedRow:
    excel_row: int
    action: str
    staging_payload: dict
    event: dict | None
    fingerprint: str | None
    errors: list[dict]


# =====================================================
# BLOQUE 2: Conversión JSON explícita para staging.
# Conserva valores de origen y contexto de archivo.
# No convierte el XLSX original ni lo reescribe.
# =====================================================
def json_safe(value):
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else str(value)
    if isinstance(value, (datetime, date, time)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    raise TypeError(f"Tipo no admitido en raw_payload: {type(value).__name__}")


# =====================================================
# BLOQUE 3: Planificar las decisiones por registro.
# Una huella identifica parámetros EXACTOS; jamás
# fusionar sismos solo por proximidad tiempo/espacio.
# =====================================================
def plan_rows(
    rows: Iterable[tuple[int, dict]],
    *,
    file_digest: str,
    known_fingerprints: Iterable[str] = (),
) -> Iterator[PlannedRow]:
    observed = set(known_fingerprints)

    for excel_row, raw in rows:
        result = normalize_igp_row(raw)
        payload = {
            "provider": "IGP",
            "file_sha256": file_digest,
            "excel_row": excel_row,
            "fingerprint_version": FINGERPRINT_VERSION,
            "record_fingerprint": result.fingerprint,
            "raw": json_safe(raw),
        }

        if result.errors:
            yield PlannedRow(
                excel_row, ACTION_INVALID, payload, None, None, result.errors
            )
        elif result.fingerprint in observed:
            yield PlannedRow(
                excel_row, ACTION_SKIP, payload, result.event,
                result.fingerprint, []
            )
        else:
            observed.add(result.fingerprint)
            yield PlannedRow(
                excel_row, ACTION_INSERT, payload, result.event,
                result.fingerprint, []
            )


# =====================================================
# BLOQUE 4: Resumen de decisiones simuladas.
# Las claves «candidates» NO son filas insertadas en BD.
# =====================================================
def summarize_plan(
    rows: Iterable[PlannedRow], *,
    capture_fingerprints: bool = False,
) -> tuple[dict, set[str]]:
    report = {
        "mode": "offline-persistence-plan",
        "database_writes": False,
        "records_seen": 0,
        "staging_candidates": 0,
        "insert_candidates": 0,
        "skip_exact_fingerprint": 0,
        "invalid_candidates": 0,
        "invalid_examples": [],
    }
    inserts: set[str] = set()
    for row in rows:
        report["records_seen"] += 1
        report["staging_candidates"] += 1
        if row.action == ACTION_INSERT:
            report["insert_candidates"] += 1
            if capture_fingerprints:
                inserts.add(row.fingerprint)
        elif row.action == ACTION_SKIP:
            report["skip_exact_fingerprint"] += 1
        elif row.action == ACTION_INVALID:
            report["invalid_candidates"] += 1
            if len(report["invalid_examples"]) < 5:
                report["invalid_examples"].append({
                    "excel_row": row.excel_row,
                    "errors": row.errors,
                })
        else:
            raise AssertionError(f"Decisión inesperada: {row.action}")

    assert report["records_seen"] == (
        report["insert_candidates"]
        + report["skip_exact_fingerprint"]
        + report["invalid_candidates"]
    )
    return report, inserts


# =====================================================
# BLOQUE 5: Simulación de dos ejecuciones independientes.
# Segunda ejecución compara contra la primera (en RAM).
# NO consulta Supabase ni comprueba concurrencia de BD.
# =====================================================
def simulate_twice(input_path: str | Path) -> dict:
    path = Path(input_path)
    file_digest = file_sha256(path)
    first, first_fingerprints = summarize_plan(
        plan_rows(iter_igp_rows(path), file_digest=file_digest),
        capture_fingerprints=True,
    )
    second, _ = summarize_plan(
        plan_rows(
            iter_igp_rows(path),
            file_digest=file_digest,
            known_fingerprints=first_fingerprints,
        ),
    )
    return {
        "mode": "offline-persistence-plan",
        "source": "IGP",
        "file_name": path.name,
        "file_sha256": file_digest,
        "database_writes": False,
        "first_run": first,
        "second_run": second,
        "warnings": [
            "Los contadores describen decisiones simuladas, no inserts reales.",
            "Una revisión de parámetros cambia la huella y podría considerarse nuevo candidato.",
            "Solo una restricción UNIQUE en PostgreSQL protege frente a carreras concurrentes.",
            "Los registros cercanos NO se fusionan automáticamente.",
        ],
    }


# =====================================================
# BLOQUE 6: Interfaz CLI para laboratorio local.
# Reportes JSON se guardan únicamente en --output.
# =====================================================
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Planificación local IGP en dos pasadas, sin base de datos"
    )
    parser.add_argument("--input", required=True, help="Ruta del XLSX original")
    parser.add_argument("--output", help="Ruta opcional para informe JSON")
    args = parser.parse_args()
    try:
        report = simulate_twice(args.input)
    except (ValueError, TypeError, FileNotFoundError, OSError) as exc:
        parser.exit(1, f"Error de planificación IGP: {exc}\n")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"\nInforme local guardado en: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
