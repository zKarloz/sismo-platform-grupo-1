"""Normalización verificable de filas IGP, sin persistencia en base de datos."""

from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json

from .reader import SOURCE_FIELDS

# =====================================================
# BLOQUE 1: Procedencia y estructura del resultado.
# La URL es del repositorio, no de un evento individual.
# =====================================================

SOURCE_NAME = "IGP"
SOURCE_URL = "https://ultimosismo.igp.gob.pe/repositorio/datos-sismicos"


@dataclass(frozen=True)
class NormalizationResult:
    event: dict | None
    fingerprint: str | None
    errors: list[dict]


# =====================================================
# BLOQUE 2: Parseadores estrictos de campos oficiales.
# No se supone una zona horaria local: el archivo dice UTC.
# =====================================================

def parse_occurrence(raw_date: object, raw_time: object) -> datetime:
    if isinstance(raw_date, datetime):
        event_date = raw_date.date()
    elif isinstance(raw_date, date):
        event_date = raw_date
    else:
        if raw_date is None:
            raise ValueError("Falta fecha UTC")
        event_date = date.fromisoformat(str(raw_date).strip())

    if isinstance(raw_time, datetime):
        event_time = raw_time.time()
    elif isinstance(raw_time, time):
        event_time = raw_time
    else:
        if raw_time is None:
            raise ValueError("Falta hora UTC")
        event_time = time.fromisoformat(str(raw_time).strip())

    if event_time.tzinfo is not None:
        raise ValueError("La hora UTC del catálogo no debe traer otra zona horaria")

    return datetime.combine(event_date, event_time, tzinfo=timezone.utc)


def parse_number(raw: object) -> Decimal:
    if raw is None or isinstance(raw, bool) or str(raw).strip() == "":
        raise ValueError("Valor numérico ausente")
    try:
        number = Decimal(str(raw).strip())
    except InvalidOperation as exc:
        raise ValueError("Valor no numérico") from exc
    if not number.is_finite():
        raise ValueError("Valor numérico no finito")
    return number


def canonical_decimal(number: Decimal) -> str:
    if number == 0:
        return "0"
    return format(number.normalize(), "f")


# =====================================================
# BLOQUE 3: Huella de versión de registro, compatible
# con la celda 11 del notebook: NO es un ID sísmico.
# Cambios de parámetros producen otra huella.
# =====================================================

def record_fingerprint(occurred_at: datetime, values: dict[str, Decimal]) -> str:
    payload = {
        "fuente": SOURCE_NAME,
        "occurred_at": occurred_at.astimezone(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        ),
        "latitude": canonical_decimal(values["latitude"]),
        "longitude": canonical_decimal(values["longitude"]),
        "depth_km": canonical_decimal(values["depth_km"]),
        "magnitude": canonical_decimal(values["magnitude"]),
    }
    source = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


# =====================================================
# BLOQUE 4: Validaciones por fila sin descartar errores.
# No imponemos magnitud máxima ni profundidad máxima:
# esos criterios científicos siguen pendientes.
# =====================================================

def normalize_igp_row(raw: dict) -> NormalizationResult:
    errors: list[dict] = []

    for column in SOURCE_FIELDS:
        if column not in raw:
            errors.append({
                "field": column,
                "code": "missing_column",
                "message": "No existe el campo esperado",
            })
    if errors:
        return NormalizationResult(None, None, errors)

    try:
        occurred_at = parse_occurrence(raw["fecha UTC"], raw["hora UTC"])
    except (ValueError, TypeError) as exc:
        errors.append({
            "field": "occurred_at", "code": "invalid_datetime", "message": str(exc)
        })
        occurred_at = None

    fields = {
        "latitude": "latitud (º)",
        "longitude": "longitud (º)",
        "depth_km": "profundidad (km)",
        "magnitude": "magnitud (M)",
    }
    numeric: dict[str, Decimal] = {}
    for target, source in fields.items():
        try:
            numeric[target] = parse_number(raw[source])
        except (ValueError, TypeError) as exc:
            errors.append({"field": target, "code": "invalid_number", "message": str(exc)})

    # Solo aplicar reglas de rango a valores numéricos válidos.
    limits = {"latitude": (-90, 90), "longitude": (-180, 180)}
    for target, (minimum, maximum) in limits.items():
        if target in numeric and not (minimum <= numeric[target] <= maximum):
            errors.append({
                "field": target, "code": "out_of_range",
                "message": f"Valor fuera de [{minimum}, {maximum}]",
            })
    if "depth_km" in numeric and numeric["depth_km"] < 0:
        errors.append({
            "field": "depth_km", "code": "negative_depth",
            "message": "Profundidad negativa; requiere revisión",
        })

    if errors:
        return NormalizationResult(None, None, errors)

    # Estos campos corresponden al esquema vigente de seismic_events.
    # source_id, id y received_at quedan reservados a la persistencia.
    event = {
        "external_id": None,
        "occurred_at": occurred_at.isoformat(),
        "latitude": float(numeric["latitude"]),
        "longitude": float(numeric["longitude"]),
        "magnitude": float(numeric["magnitude"]),
        "magnitude_type": None,
        "depth_km": float(numeric["depth_km"]),
        "place": None,
        "source_url": SOURCE_URL,
        "review_status": "pending",
    }
    return NormalizationResult(event, record_fingerprint(occurred_at, numeric), [])
