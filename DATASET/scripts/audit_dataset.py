#!/usr/bin/env python3
"""Audita el dataset canonico sin modificarlo ni abrir archivos Blender."""

from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATASET = ROOT / "dataset_v2_with_blends_with_depth.json"
DEFAULT_JSON_REPORT = ROOT / "reports" / "dataset_audit_creation_v1.json"
DEFAULT_MD_REPORT = ROOT / "reports" / "dataset_audit_creation_v1.md"
ID_PATTERN = re.compile(r"^p(\d+)$")
REQUIRED_TEXT_FIELDS = ("prompt", "python_code")
REQUIRED_ARTIFACT_FIELDS = ("blend_path", "render_path", "depth_path")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Auditoria no destructiva del dataset de creacion"
    )
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--json-report", type=Path, default=DEFAULT_JSON_REPORT)
    parser.add_argument("--md-report", type=Path, default=DEFAULT_MD_REPORT)
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def resolve_artifact(dataset_path: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return (dataset_path.parent / path).resolve()


def duplicate_groups(values: dict[str, str]) -> list[dict[str, Any]]:
    groups: dict[str, list[str]] = defaultdict(list)
    originals: dict[str, str] = {}
    for item_id, value in values.items():
        key = normalized_text(value)
        groups[key].append(item_id)
        originals.setdefault(key, value)
    return [
        {
            "item_ids": item_ids,
            "count": len(item_ids),
            "sample": originals[key][:500],
        }
        for key, item_ids in groups.items()
        if len(item_ids) > 1
    ]


def audit(dataset_path: Path) -> dict[str, Any]:
    dataset_path = dataset_path.resolve()
    data = json.loads(dataset_path.read_text(encoding="utf-8"))
    meta = data.get("meta", {})
    items = data.get("items", {})
    if not isinstance(items, dict):
        raise ValueError("El campo 'items' debe ser un objeto JSON")

    domains: Counter[str] = Counter()
    tiers: Counter[str] = Counter()
    complexities: Counter[str] = Counter()
    categories: Counter[str] = Counter()
    missing_fields: dict[str, list[str]] = defaultdict(list)
    missing_artifacts: dict[str, list[str]] = defaultdict(list)
    invalid_python: dict[str, str] = {}
    prompts: dict[str, str] = {}
    code_by_hash: dict[str, list[str]] = defaultdict(list)
    numeric_ids: list[int] = []
    invalid_ids: list[str] = []
    object_counts: list[int] = []

    for item_id, item in items.items():
        if not isinstance(item, dict):
            missing_fields["invalid_item_object"].append(item_id)
            continue

        id_match = ID_PATTERN.fullmatch(item_id)
        if id_match:
            numeric_ids.append(int(id_match.group(1)))
        else:
            invalid_ids.append(item_id)

        domains[str(item.get("domain", "<missing>"))] += 1
        tiers[str(item.get("tier", "<missing>"))] += 1
        complexities[str(item.get("complexity", "<missing>"))] += 1
        categories[str(item.get("category", "<missing>"))] += 1

        objects = item.get("objects")
        if isinstance(objects, list):
            object_counts.append(len(objects))
        else:
            missing_fields["objects"].append(item_id)

        if not str(item.get("asset_collection", "")).strip():
            missing_fields["asset_collection"].append(item_id)

        for field in REQUIRED_TEXT_FIELDS:
            value = item.get(field)
            if not isinstance(value, str) or not value.strip():
                missing_fields[field].append(item_id)

        prompt = item.get("prompt")
        if isinstance(prompt, str) and prompt.strip():
            prompts[item_id] = prompt

        code = item.get("python_code")
        if isinstance(code, str) and code.strip():
            try:
                ast.parse(code)
            except SyntaxError as error:
                invalid_python[item_id] = (
                    f"line {error.lineno}, column {error.offset}: {error.msg}"
                )
            code_hash = hashlib.sha256(code.strip().encode("utf-8")).hexdigest()
            code_by_hash[code_hash].append(item_id)

        for field in REQUIRED_ARTIFACT_FIELDS:
            value = item.get(field)
            if not isinstance(value, str) or not value.strip():
                missing_fields[field].append(item_id)
                continue
            if not resolve_artifact(dataset_path, value).is_file():
                missing_artifacts[field].append(item_id)

    numeric_ids.sort()
    id_min = numeric_ids[0] if numeric_ids else None
    id_max = numeric_ids[-1] if numeric_ids else None
    missing_numeric_ids = []
    if id_min is not None and id_max is not None:
        missing_numeric_ids = sorted(set(range(id_min, id_max + 1)) - set(numeric_ids))

    exact_prompt_duplicates = duplicate_groups(prompts)
    exact_code_duplicates = [
        {"sha256": code_hash, "count": len(ids), "item_ids": ids}
        for code_hash, ids in code_by_hash.items()
        if len(ids) > 1
    ]

    out_assets = dataset_path.parent / "out_assets"
    asset_dirs = {
        path.name
        for path in out_assets.iterdir()
        if path.is_dir() and ID_PATTERN.fullmatch(path.name)
    } if out_assets.is_dir() else set()
    item_ids = set(items)

    actual_counts = {
        "total": len(items),
        "domains": dict(sorted(domains.items())),
        "tiers": dict(sorted(tiers.items())),
        "complexities": dict(sorted(complexities.items())),
        "categories": dict(categories.most_common()),
    }
    declared_counts = {
        "total": meta.get("total"),
        "tiers": meta.get("tiers", {}),
        "balance": meta.get("balance", {}),
    }
    metadata_mismatches = {
        "total": declared_counts["total"] != actual_counts["total"],
        "tiers": declared_counts["tiers"] != actual_counts["tiers"],
        "balance": declared_counts["balance"] != actual_counts["domains"],
    }

    warnings = []
    if any(metadata_mismatches.values()):
        warnings.append("Los contadores de meta no coinciden con el contenido real.")
    if missing_numeric_ids:
        warnings.append("La secuencia de IDs contiene huecos; no implica por si solo un error.")
    if asset_dirs - item_ids:
        warnings.append("Existen directorios de activos no referenciados por el dataset.")
    if exact_code_duplicates:
        warnings.append("Existen programas Python exactamente duplicados.")
    warnings.append(
        "Esta auditoria no demuestra validez geometrica ni cumplimiento semantico."
    )

    return {
        "audit": {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "dataset_path": str(dataset_path),
            "dataset_sha256": sha256_file(dataset_path),
            "scope": "static_non_destructive",
        },
        "declared_counts": declared_counts,
        "actual_counts": actual_counts,
        "metadata_mismatches": metadata_mismatches,
        "fields": {
            "missing": {key: value for key, value in sorted(missing_fields.items())},
            "missing_counts": {
                key: len(value) for key, value in sorted(missing_fields.items())
            },
        },
        "python": {
            "valid_count": len(items) - len(invalid_python),
            "invalid_count": len(invalid_python),
            "invalid_items": invalid_python,
        },
        "artifacts": {
            "missing": {key: value for key, value in sorted(missing_artifacts.items())},
            "missing_counts": {
                key: len(value) for key, value in sorted(missing_artifacts.items())
            },
            "asset_directory_count": len(asset_dirs),
            "orphan_asset_directory_count": len(asset_dirs - item_ids),
            "orphan_asset_directories": sorted(asset_dirs - item_ids),
            "items_without_asset_directory_count": len(item_ids - asset_dirs),
            "items_without_asset_directory": sorted(item_ids - asset_dirs),
        },
        "ids": {
            "valid_count": len(numeric_ids),
            "invalid": invalid_ids,
            "min": id_min,
            "max": id_max,
            "gap_count": len(missing_numeric_ids),
            "gaps": [f"p{number:04d}" for number in missing_numeric_ids],
        },
        "duplicates": {
            "exact_prompt_group_count": len(exact_prompt_duplicates),
            "exact_prompt_groups": exact_prompt_duplicates,
            "exact_code_group_count": len(exact_code_duplicates),
            "exact_code_groups": exact_code_duplicates,
        },
        "objects": {
            "items_with_object_list": len(object_counts),
            "min_per_item": min(object_counts) if object_counts else None,
            "max_per_item": max(object_counts) if object_counts else None,
            "total_references": sum(object_counts),
        },
        "warnings": warnings,
    }


def format_mapping(mapping: dict[str, Any]) -> str:
    if not mapping:
        return "- Ninguno."
    return "\n".join(f"- `{key}`: {value}" for key, value in mapping.items())


def markdown_report(report: dict[str, Any]) -> str:
    actual = report["actual_counts"]
    declared = report["declared_counts"]
    artifacts = report["artifacts"]
    duplicates = report["duplicates"]
    objects = report["objects"]
    top_categories = dict(list(actual["categories"].items())[:20])
    warning_lines = "\n".join(f"- {warning}" for warning in report["warnings"])

    return f"""# Auditoria del dataset de creacion v1

Generada: `{report['audit']['created_at']}`

Dataset: `{report['audit']['dataset_path']}`

SHA-256: `{report['audit']['dataset_sha256']}`

## Resumen

| Comprobacion | Declarado | Real |
|---|---:|---:|
| Total | {declared['total']} | {actual['total']} |
| Scripts Python validos | - | {report['python']['valid_count']} |
| Scripts Python invalidos | - | {report['python']['invalid_count']} |
| Directorios de activos | - | {artifacts['asset_directory_count']} |
| Directorios huerfanos | - | {artifacts['orphan_asset_directory_count']} |
| Huecos en IDs | - | {report['ids']['gap_count']} |
| Grupos de prompts duplicados | - | {duplicates['exact_prompt_group_count']} |
| Grupos de codigo duplicado | - | {duplicates['exact_code_group_count']} |

## Dominios reales

{format_mapping(actual['domains'])}

## Tiers reales

{format_mapping(actual['tiers'])}

## Complejidad real

{format_mapping(actual['complexities'])}

## Principales categorias

{format_mapping(top_categories)}

## Campos faltantes

{format_mapping(report['fields']['missing_counts'])}

## Artefactos faltantes

{format_mapping(artifacts['missing_counts'])}

## Referencias de objetos

- Items con lista de objetos: {objects['items_with_object_list']}
- Referencias totales: {objects['total_references']}
- Minimo por item: {objects['min_per_item']}
- Maximo por item: {objects['max_per_item']}

## Advertencias

{warning_lines}

## Alcance

Este reporte verifica estructura, rutas, sintaxis, duplicados exactos y consistencia de
metadatos. No abre los `.blend` y no demuestra validez geometrica, exactitud dimensional
ni cumplimiento semantico del prompt. Esas comprobaciones corresponden a la siguiente
etapa de la Prioridad 2.
"""


def write_report(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    args = parse_args()
    report = audit(args.dataset)
    write_report(
        args.json_report,
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
    )
    write_report(args.md_report, markdown_report(report))
    print(f"Dataset auditado: {report['actual_counts']['total']} items")
    print(f"Reporte JSON: {args.json_report.resolve()}")
    print(f"Reporte Markdown: {args.md_report.resolve()}")


if __name__ == "__main__":
    main()
