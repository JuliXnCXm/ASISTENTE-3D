#!/usr/bin/env python3
"""Construye una copia canonica y versionada sin modificar el dataset fuente."""

from __future__ import annotations

import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import unicodedata
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = ROOT.parent
DEFAULT_SOURCE = ROOT / "dataset_v2_with_blends_with_depth.json"
DEFAULT_OUTPUT = ROOT / "dataset_creation_v1.json"
DEFAULT_SCHEMA = ROOT / "schema" / "dataset_creation_v1.schema.json"
DEFAULT_TAXONOMY = ROOT / "schema" / "category_taxonomy_v1.json"
DEFAULT_MANIFEST = ROOT / "reports" / "dataset_creation_v1_manifest.json"
DEFAULT_NORMALIZATION_REPORT = ROOT / "reports" / "category_normalization_v1.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Construye dataset_creation_v1 a partir del dataset fuente"
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--taxonomy", type=Path, default=DEFAULT_TAXONOMY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--normalization-report",
        type=Path,
        default=DEFAULT_NORMALIZATION_REPORT,
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Permite reemplazar salidas canonicas existentes",
    )
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def portable_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


def normalized_label(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return "_".join(ascii_value.strip().lower().replace("-", " ").replace("_", " ").split())


def load_taxonomy(path: Path) -> tuple[dict[str, str], list[str], str]:
    taxonomy = json.loads(path.read_text(encoding="utf-8"))
    categories = taxonomy.get("categories", {})
    if not isinstance(categories, dict) or not categories:
        raise ValueError("La taxonomia no contiene categorias")

    alias_map: dict[str, str] = {}
    for canonical, aliases in categories.items():
        for alias in [canonical, *aliases]:
            key = normalized_label(alias)
            previous = alias_map.get(key)
            if previous and previous != canonical:
                raise ValueError(
                    f"Alias ambiguo '{alias}': {previous} y {canonical}"
                )
            alias_map[key] = canonical
    return alias_map, sorted(categories), str(taxonomy.get("taxonomy_version", "unknown"))


def resolve_artifact(dataset_path: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return (dataset_path.parent / path).resolve()


def execution_status(dataset_path: Path, blend_path: str) -> str:
    log_path = resolve_artifact(dataset_path, blend_path).parent / "run.log"
    if not log_path.is_file():
        return "not_revalidated"
    first_line = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    if not first_line:
        return "not_revalidated"
    if first_line[0].startswith("OK"):
        return "historical_success"
    if first_line[0].startswith("ERROR"):
        return "historical_failure"
    return "not_revalidated"


def canonical_item(
    item_id: str,
    item: dict[str, Any],
    source_path: Path,
    alias_map: dict[str, str],
) -> tuple[dict[str, Any], str]:
    original_category = str(item.get("category", "")).strip()
    normalized_category = alias_map.get(normalized_label(original_category))
    if not normalized_category:
        raise ValueError(
            f"Categoria sin mapear en {item_id}: {original_category!r}"
        )

    code = str(item.get("python_code", ""))
    try:
        ast.parse(code)
        syntax_status = "valid"
    except SyntaxError:
        syntax_status = "invalid"

    artifact_complete = all(
        isinstance(item.get(field), str)
        and resolve_artifact(source_path, item[field]).is_file()
        for field in ("blend_path", "render_path", "depth_path")
    )

    result = {
        "id": item_id,
        "task_type": "creation",
        "domain": item.get("domain"),
        "category": normalized_category,
        "category_original": original_category,
        "complexity": item.get("complexity"),
        "tier": item.get("tier"),
        "prompt": item.get("prompt"),
        "python_code": code,
        "blend_path": item.get("blend_path"),
        "render_path": item.get("render_path"),
        "depth_path": item.get("depth_path"),
        "asset_collection": item.get("asset_collection"),
        "objects": item.get("objects"),
        "units": "m",
        "coordinate_system": "RH_Z_UP",
        "split": None,
        "family_id": None,
        "validation": {
            "syntax_status": syntax_status,
            "artifact_status": "complete" if artifact_complete else "incomplete",
            "execution_status": execution_status(source_path, str(item.get("blend_path", ""))),
            "geometry_status": "not_evaluated",
            "semantic_status": "not_evaluated",
        },
    }
    return result, normalized_category


def validate_internal(dataset: dict[str, Any], allowed_categories: set[str]) -> None:
    meta = dataset["meta"]
    items = dataset["items"]
    if meta["total"] != len(items):
        raise ValueError("meta.total no coincide con items")
    if sum(meta["tiers"].values()) != len(items):
        raise ValueError("La suma de tiers no coincide con items")
    if sum(meta["balance"].values()) != len(items):
        raise ValueError("La suma del balance no coincide con items")
    if sum(meta["complexities"].values()) != len(items):
        raise ValueError("La suma de complejidades no coincide con items")
    if sum(meta["categories"].values()) != len(items):
        raise ValueError("La suma de categorias no coincide con items")

    for item_id, item in items.items():
        if item["id"] != item_id:
            raise ValueError(f"ID interno inconsistente: {item_id}")
        if item["category"] not in allowed_categories:
            raise ValueError(f"Categoria no permitida: {item['category']}")
        if item["validation"]["syntax_status"] != "valid":
            raise ValueError(f"Codigo invalido en {item_id}")
        if item["validation"]["artifact_status"] != "complete":
            raise ValueError(f"Artefactos incompletos en {item_id}")


def validate_json_schema(dataset: dict[str, Any], schema_path: Path) -> str:
    try:
        import jsonschema
    except ImportError:
        return "not_run_jsonschema_not_installed"

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(
        schema,
        format_checker=jsonschema.FormatChecker(),
    )
    errors = sorted(validator.iter_errors(dataset), key=lambda error: list(error.path))
    if errors:
        details = "\n".join(
            f"- {'/'.join(map(str, error.path))}: {error.message}"
            for error in errors[:20]
        )
        raise ValueError(f"El dataset no cumple el JSON Schema:\n{details}")
    return "passed"


def ensure_writable(paths: list[Path], force: bool) -> None:
    if force:
        return
    existing = [str(path) for path in paths if path.exists()]
    if existing:
        raise FileExistsError(
            "Las siguientes salidas ya existen; usa --force para reemplazarlas: "
            + ", ".join(existing)
        )


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def normalization_markdown(
    source_categories: Counter[str],
    normalized_counts: Counter[str],
    alias_map: dict[str, str],
) -> str:
    mappings = sorted(
        (
            source,
            alias_map[normalized_label(source)],
            count,
        )
        for source, count in source_categories.items()
    )
    mapping_rows = "\n".join(
        f"| `{source}` | `{canonical}` | {count} |"
        for source, canonical, count in mappings
    )
    normalized_rows = "\n".join(
        f"- `{category}`: {count}"
        for category, count in normalized_counts.most_common()
    )
    return f"""# Normalizacion de categorias v1

La normalizacion conserva la etiqueta de origen en `category_original` y utiliza
`category` para la taxonomia canonica. No se eliminaron elementos por su categoria.

## Distribucion canonica

{normalized_rows}

## Mapeo aplicado

| Categoria original | Categoria canonica | Items |
|---|---|---:|
{mapping_rows}
"""


def main() -> None:
    args = parse_args()
    source_path = args.source.resolve()
    output_path = args.output.resolve()
    schema_path = args.schema.resolve()
    taxonomy_path = args.taxonomy.resolve()
    manifest_path = args.manifest.resolve()
    normalization_report_path = args.normalization_report.resolve()

    ensure_writable(
        [output_path, manifest_path, normalization_report_path],
        args.force,
    )

    source = json.loads(source_path.read_text(encoding="utf-8"))
    source_items = source.get("items", {})
    if not isinstance(source_items, dict) or not source_items:
        raise ValueError("El dataset fuente no contiene items validos")

    alias_map, allowed_categories, taxonomy_version = load_taxonomy(taxonomy_path)
    canonical_items: dict[str, dict[str, Any]] = {}
    source_categories: Counter[str] = Counter()
    domains: Counter[str] = Counter()
    tiers: Counter[str] = Counter()
    complexities: Counter[str] = Counter()
    normalized_categories: Counter[str] = Counter()

    for item_id, source_item in source_items.items():
        item, normalized_category = canonical_item(
            item_id,
            source_item,
            source_path,
            alias_map,
        )
        canonical_items[item_id] = item
        source_categories[item["category_original"]] += 1
        normalized_categories[normalized_category] += 1
        domains[str(item["domain"])] += 1
        tiers[str(item["tier"])] += 1
        complexities[str(item["complexity"])] += 1

    source_meta = source.get("meta", {})
    canonical = {
        "meta": {
            "schema_version": "1.0.0",
            "dataset_version": "creation-v1.0.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_dataset": source_path.name,
            "source_dataset_sha256": sha256_file(source_path),
            "source_updated_at": source_meta.get("updated_at"),
            "model": str(source_meta.get("model", "unknown")),
            "language": "es",
            "task_type": "creation",
            "representation": "procedural_parametric_mesh",
            "units": "m",
            "coordinate_system": "RH_Z_UP",
            "blender_version": "not_recorded",
            "dsl_version": "unversioned",
            "total": len(canonical_items),
            "tiers": dict(sorted(tiers.items())),
            "balance": dict(sorted(domains.items())),
            "complexities": dict(sorted(complexities.items())),
            "categories": dict(normalized_categories.most_common()),
            "artifact_fields": ["blend_path", "render_path", "depth_path"],
            "depth_status": "normalized_preview_without_metric_reconstruction_metadata",
        },
        "items": canonical_items,
    }

    validate_internal(canonical, set(allowed_categories))
    schema_validation = validate_json_schema(canonical, schema_path)
    write_json(output_path, canonical)

    normalization_report_path.parent.mkdir(parents=True, exist_ok=True)
    normalization_report_path.write_text(
        normalization_markdown(source_categories, normalized_categories, alias_map),
        encoding="utf-8",
    )

    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "dataset_version": canonical["meta"]["dataset_version"],
        "schema_version": canonical["meta"]["schema_version"],
        "taxonomy_version": taxonomy_version,
        "source": {
            "path": portable_path(source_path),
            "sha256": sha256_file(source_path),
        },
        "canonical": {
            "path": portable_path(output_path),
            "sha256": sha256_file(output_path),
            "total": len(canonical_items),
        },
        "schema": {
            "path": portable_path(schema_path),
            "sha256": sha256_file(schema_path),
            "validation": schema_validation,
        },
        "taxonomy": {
            "path": portable_path(taxonomy_path),
            "sha256": sha256_file(taxonomy_path),
            "canonical_category_count": len(allowed_categories),
            "source_category_count": len(source_categories),
        },
        "validation_scope": {
            "syntax": "validated",
            "artifacts": "paths_and_files_validated",
            "execution": "historical_logs_only",
            "geometry": "not_evaluated",
            "semantics": "not_evaluated"
        }
    }
    write_json(manifest_path, manifest)

    print(f"Dataset canonico: {output_path}")
    print(f"Items: {len(canonical_items)}")
    print(f"Categorias originales: {len(source_categories)}")
    print(f"Categorias canonicas: {len(allowed_categories)}")
    print(f"Validacion JSON Schema: {schema_validation}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
