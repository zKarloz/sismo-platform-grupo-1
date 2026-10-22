"""CLI para evaluar el catálogo IGP sin conexión ni escrituras a Supabase."""

import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path

from .normalizer import SOURCE_NAME, SOURCE_URL, normalize_igp_row
from .reader import iter_igp_rows

# =====================================================
# BLOQUE 1: Huella del archivo completo para procedencia.
# =====================================================

def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for piece in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(piece)
    return digest.hexdigest()


# =====================================================
# BLOQUE 2: Resumen sin exponer el dataset ni conectarse
# a la base de datos. Las filas inválidas se contabilizan;
# nunca se descartan silenciosamente.
# =====================================================

def run_dry_run(path: str | Path) -> dict:
    input_path = Path(path)
    report = {
        "mode": "dry-run",
        "database_writes": False,
        "source": SOURCE_NAME,
        "source_url": SOURCE_URL,
        "file_name": input_path.name,
        "file_sha256": file_sha256(input_path),
        "records_seen": 0,
        "records_valid": 0,
        "records_invalid": 0,
        "unique_record_fingerprints": 0,
        "repeated_record_fingerprints": 0,
        "events_by_year": {},
        "earliest_event_utc": None,
        "latest_event_utc": None,
        "valid_examples": [],
        "invalid_examples": [],
        "repeated_examples": [],
        "observations": [
            "Las huellas identifican versiones exactas de registros, no eventos estables.",
            "No se determina si dos eventos próximos son un mismo sismo.",
            "No se asignan source_id, external_id ni IDs internos.",
        ],
    }
    seen_fingerprints: dict[str, int] = {}
    years: Counter[int] = Counter()

    for excel_row, raw in iter_igp_rows(input_path):
        report["records_seen"] += 1
        result = normalize_igp_row(raw)
        if result.errors:
            report["records_invalid"] += 1
            if len(report["invalid_examples"]) < 10:
                report["invalid_examples"].append({
                    "excel_row": excel_row, "errors": result.errors,
                })
            continue

        report["records_valid"] += 1
        event = result.event
        fingerprint = result.fingerprint
        if fingerprint in seen_fingerprints:
            report["repeated_record_fingerprints"] += 1
            if len(report["repeated_examples"]) < 10:
                report["repeated_examples"].append({
                    "excel_row": excel_row,
                    "first_excel_row": seen_fingerprints[fingerprint],
                    "fingerprint": fingerprint,
                })
        else:
            seen_fingerprints[fingerprint] = excel_row

        instant = event["occurred_at"]
        years[datetime.fromisoformat(instant).year] += 1
        if report["earliest_event_utc"] is None or instant < report["earliest_event_utc"]:
            report["earliest_event_utc"] = instant
        if report["latest_event_utc"] is None or instant > report["latest_event_utc"]:
            report["latest_event_utc"] = instant
        if len(report["valid_examples"]) < 3:
            report["valid_examples"].append({
                "excel_row": excel_row, "fingerprint": fingerprint, "event": event,
            })

    report["unique_record_fingerprints"] = len(seen_fingerprints)
    report["events_by_year"] = {str(year): years[year] for year in sorted(years)}
    assert report["records_seen"] == report["records_valid"] + report["records_invalid"]
    return report


# =====================================================
# BLOQUE 3: Entrada de línea de comandos; --output solo
# guarda un resumen JSON local cuando se solicita.
# =====================================================

def main() -> int:
    parser = argparse.ArgumentParser(description="Auditoría de ingesta IGP, sin Supabase")
    parser.add_argument("--input", required=True, help="Ruta al Excel original IGP")
    parser.add_argument("--output", help="Ruta opcional al resumen JSON local")
    args = parser.parse_args()
    try:
        report = run_dry_run(args.input)
        # Vista de consola compacta. El informe JSON opcional mantiene
        # el detalle completo para documentación y pruebas.
        summary_keys = (
            "mode", "database_writes", "source", "file_name", "file_sha256",
            "records_seen", "records_valid", "records_invalid",
            "unique_record_fingerprints", "repeated_record_fingerprints",
            "earliest_event_utc", "latest_event_utc",
        )
        summary = {key: report[key] for key in summary_keys}
        summary["records_2024"] = report["events_by_year"].get("2024", 0)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        if args.output:
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            print(f"\nInforme local guardado en: {output}")
        return 0 if report["records_invalid"] == 0 else 2
    except (FileNotFoundError, ValueError, OSError) as exc:
        parser.exit(1, f"Error de lectura o contrato IGP: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
