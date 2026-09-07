#!/usr/bin/env python3
"""Detecta familias generativas y propone splits sin modificar el dataset."""

from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
import hashlib
import json
import math
from pathlib import Path
import re
import unicodedata
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = ROOT.parent
DEFAULT_DATASET = ROOT / "dataset_creation_v1.json"
DEFAULT_MANIFEST = ROOT / "splits" / "creation_v1_splits.json"
DEFAULT_JSON_REPORT = ROOT / "reports" / "dataset_families_v1.json"
DEFAULT_MD_REPORT = ROOT / "reports" / "dataset_families_v1.md"
SPLIT_RATIOS = {"train": 0.70, "validation": 0.15, "test": 0.15}

NUMBER_RE = re.compile(r"(?<![a-z])\d+(?:[.,]\d+)?(?:\s*[x×]\s*\d+(?:[.,]\d+)?)*", re.I)
WORD_RE = re.compile(r"[a-záéíóúüñ<>]+", re.I)
CREATION_VERBS = {
    "crea", "crear", "construye", "construir", "disena", "disenar",
    "genera", "generar", "levanta", "levantar", "modela", "modelar",
}
STOPWORDS = {
    "a", "al", "con", "de", "del", "el", "en", "es", "esta", "este",
    "la", "las", "lo", "los", "para", "por", "que", "se", "ser", "su",
    "sus", "un", "una", "uno", "unos", "unas", "y",
}
UNIT_WORDS = {
    "cm", "centimetro", "centimetros", "m", "metro", "metros", "mm",
    "milimetro", "milimetros",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Agrupa familias y propone train/validation/test"
    )
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--json-report", type=Path, default=DEFAULT_JSON_REPORT)
    parser.add_argument("--md-report", type=Path, default=DEFAULT_MD_REPORT)
    parser.add_argument("--prompt-jaccard", type=float, default=0.82)
    parser.add_argument("--prompt-sequence", type=float, default=0.92)
    parser.add_argument("--seed", type=int, default=20250905)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Permite reemplazar reportes y manifiesto existentes",
    )
    return parser.parse_args()


def portable_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ascii_text(value: str) -> str:
    return unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()


def normalized_prompt(value: str) -> str:
    text = ascii_text(value).lower()
    text = NUMBER_RE.sub(" <num> ", text)
    words = WORD_RE.findall(text)
    normalized = []
    for word in words:
        if word in CREATION_VERBS:
            word = "crear"
        if word in UNIT_WORDS:
            word = "<unit>"
        normalized.append(word)
    return " ".join(normalized)


def prompt_features(value: str) -> frozenset[str]:
    words = [
        word
        for word in normalized_prompt(value).split()
        if word not in STOPWORDS
    ]
    features = {f"w:{word}" for word in words}
    features.update(
        f"b:{left}_{right}"
        for left, right in zip(words, words[1:])
    )
    return frozenset(features)


def jaccard(left: frozenset[str], right: frozenset[str]) -> float:
    if not left and not right:
        return 1.0
    union = left | right
    return len(left & right) / len(union) if union else 0.0


class AstTemplateNormalizer(ast.NodeTransformer):
    """Elimina nombres y valores, pero conserva operaciones y APIs usadas."""

    def visit_Name(self, node: ast.Name) -> ast.AST:
        return ast.copy_location(ast.Name(id="_name", ctx=node.ctx), node)

    def visit_arg(self, node: ast.arg) -> ast.AST:
        node.arg = "_arg"
        return self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        node.name = "_function"
        return self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AST:
        node.name = "_function"
        return self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        if node.value is None or isinstance(node.value, bool):
            value: Any = node.value
        elif isinstance(node.value, str):
            value = "<str>"
        elif isinstance(node.value, (int, float, complex)):
            value = 0
        elif isinstance(node.value, bytes):
            value = b"<bytes>"
        else:
            value = "<constant>"
        return ast.copy_location(ast.Constant(value=value), node)


def ast_template_hash(code: str) -> str:
    tree = ast.parse(code)
    normalized = AstTemplateNormalizer().visit(tree)
    ast.fix_missing_locations(normalized)
    dump = ast.dump(normalized, annotate_fields=True, include_attributes=False)
    return hashlib.sha256(dump.encode("utf-8")).hexdigest()


def exact_code_hash(code: str) -> str:
    return hashlib.sha256(code.strip().encode("utf-8")).hexdigest()


class UnionFind:
    def __init__(self, values: Iterable[str]) -> None:
        self.parent = {value: value for value in values}
        self.rank = {value: 0 for value in values}

    def find(self, value: str) -> str:
        parent = self.parent[value]
        if parent != value:
            self.parent[value] = self.find(parent)
        return self.parent[value]

    def union(self, left: str, right: str) -> bool:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root == right_root:
            return False
        if self.rank[left_root] < self.rank[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        if self.rank[left_root] == self.rank[right_root]:
            self.rank[left_root] += 1
        return True


@dataclass(frozen=True)
class SimilarPair:
    left: str
    right: str
    jaccard: float
    sequence: float


def union_group(
    union_find: UnionFind,
    item_ids: list[str],
    edge_counter: Counter[str],
    reason: str,
) -> None:
    if len(item_ids) < 2:
        return
    anchor = item_ids[0]
    for item_id in item_ids[1:]:
        if union_find.union(anchor, item_id):
            edge_counter[reason] += 1


def detect_families(
    items: dict[str, dict[str, Any]],
    prompt_jaccard_threshold: float,
    prompt_sequence_threshold: float,
) -> tuple[dict[str, list[str]], dict[str, Any]]:
    union_find = UnionFind(items)
    edge_counter: Counter[str] = Counter()
    exact_code_groups: dict[str, list[str]] = defaultdict(list)
    ast_groups: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    prompt_template_groups: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    strata: dict[tuple[str, str], list[str]] = defaultdict(list)
    normalized_prompts: dict[str, str] = {}
    features: dict[str, frozenset[str]] = {}

    for item_id, item in items.items():
        code = str(item["python_code"])
        prompt = str(item["prompt"])
        category = str(item["category"])
        domain = str(item["domain"])
        exact_code_groups[exact_code_hash(code)].append(item_id)
        ast_groups[(domain, category, ast_template_hash(code))].append(item_id)
        normalized = normalized_prompt(prompt)
        normalized_prompts[item_id] = normalized
        features[item_id] = prompt_features(prompt)
        prompt_template_groups[(domain, category, normalized)].append(item_id)
        strata[(domain, category)].append(item_id)

    for group in exact_code_groups.values():
        union_group(union_find, sorted(group), edge_counter, "exact_code")
    for group in ast_groups.values():
        union_group(union_find, sorted(group), edge_counter, "ast_template")
    for group in prompt_template_groups.values():
        union_group(union_find, sorted(group), edge_counter, "prompt_template")

    similar_pairs: list[SimilarPair] = []
    compared_pairs = 0
    for stratum_ids in strata.values():
        ordered = sorted(stratum_ids)
        for index, left in enumerate(ordered):
            for right in ordered[index + 1:]:
                compared_pairs += 1
                similarity = jaccard(features[left], features[right])
                sequence = 0.0
                if similarity >= 0.55:
                    sequence = SequenceMatcher(
                        None,
                        normalized_prompts[left],
                        normalized_prompts[right],
                        autojunk=False,
                    ).ratio()
                if (
                    similarity >= prompt_jaccard_threshold
                    or sequence >= prompt_sequence_threshold
                ):
                    if union_find.union(left, right):
                        edge_counter["prompt_similarity"] += 1
                    similar_pairs.append(
                        SimilarPair(left, right, similarity, sequence)
                    )

    components: dict[str, list[str]] = defaultdict(list)
    for item_id in sorted(items):
        components[union_find.find(item_id)].append(item_id)

    ordered_components = sorted(
        (sorted(component) for component in components.values()),
        key=lambda component: component[0],
    )
    families = {
        "fam_" + hashlib.sha256("|".join(component).encode()).hexdigest()[:12]: component
        for component in ordered_components
    }
    largest_ast_groups = sorted(
        (len(group), key[0], key[1], key[2], sorted(group))
        for key, group in ast_groups.items()
        if len(group) > 1
    )[-20:][::-1]

    details = {
        "edge_counts": dict(sorted(edge_counter.items())),
        "prompt_pairs_compared": compared_pairs,
        "prompt_similar_pair_count": len(similar_pairs),
        "prompt_similar_pairs": [
            {
                "left": pair.left,
                "right": pair.right,
                "jaccard": round(pair.jaccard, 4),
                "sequence": round(pair.sequence, 4),
                "left_prompt": items[pair.left]["prompt"],
                "right_prompt": items[pair.right]["prompt"],
            }
            for pair in sorted(
                similar_pairs,
                key=lambda pair: max(pair.jaccard, pair.sequence),
                reverse=True,
            )[:200]
        ],
        "largest_ast_template_groups": [
            {
                "size": size,
                "domain": domain,
                "category": category,
                "ast_template_sha256": fingerprint,
                "item_ids": item_ids,
            }
            for size, domain, category, fingerprint, item_ids in largest_ast_groups
        ],
    }
    return families, details


def family_attributes(
    family: list[str],
    items: dict[str, dict[str, Any]],
) -> Counter[tuple[str, str]]:
    attributes: Counter[tuple[str, str]] = Counter()
    for item_id in family:
        item = items[item_id]
        attributes[("domain", str(item["domain"]))] += 1
        attributes[("category", str(item["category"]))] += 1
        attributes[("tier", str(item["tier"]))] += 1
        attributes[("complexity", str(item["complexity"]))] += 1
    return attributes


def deterministic_tie(family_id: str, split: str, seed: int) -> float:
    value = hashlib.sha256(f"{seed}:{family_id}:{split}".encode()).digest()
    return int.from_bytes(value[:8], "big") / 2**64


def propose_splits(
    families: dict[str, list[str]],
    items: dict[str, dict[str, Any]],
    seed: int,
) -> tuple[dict[str, str], dict[str, Any]]:
    total_items = len(items)
    total_attributes: Counter[tuple[str, str]] = Counter()
    attributes_by_family = {}
    for family_id, family in families.items():
        attributes = family_attributes(family, items)
        attributes_by_family[family_id] = attributes
        total_attributes.update(attributes)

    split_sizes: Counter[str] = Counter()
    split_attributes = {
        split: Counter() for split in SPLIT_RATIOS
    }
    family_assignments: dict[str, str] = {}

    ordered_families = sorted(
        families,
        key=lambda family_id: (
            -len(families[family_id]),
            deterministic_tie(family_id, "order", seed),
        ),
    )

    for family_id in ordered_families:
        family_size = len(families[family_id])
        attributes = attributes_by_family[family_id]
        candidates = []
        for split, ratio in SPLIT_RATIOS.items():
            score = 0.0
            for current_split, current_ratio in SPLIT_RATIOS.items():
                size = split_sizes[current_split]
                if current_split == split:
                    size += family_size
                target = total_items * current_ratio
                score += 4.0 * ((size - target) / max(target, 1.0)) ** 2

            for attribute, family_count in attributes.items():
                attribute_total = total_attributes[attribute]
                for current_split, current_ratio in SPLIT_RATIOS.items():
                    count = split_attributes[current_split][attribute]
                    if current_split == split:
                        count += family_count
                    target = attribute_total * current_ratio
                    score += ((count - target) / max(target, 1.0)) ** 2

            projected = split_sizes[split] + family_size
            target = total_items * ratio
            if projected > target:
                score += 3.0 * ((projected - target) / max(target, 1.0)) ** 2
            candidates.append(
                (score, deterministic_tie(family_id, split, seed), split)
            )

        _, _, selected = min(candidates)
        family_assignments[family_id] = selected
        split_sizes[selected] += family_size
        split_attributes[selected].update(attributes)

    item_assignments = {
        item_id: {
            "family_id": family_id,
            "split": family_assignments[family_id],
        }
        for family_id, family in families.items()
        for item_id in family
    }

    summary = {
        "item_counts": dict(sorted(split_sizes.items())),
        "family_counts": dict(sorted(Counter(family_assignments.values()).items())),
        "distributions": {},
    }
    for attribute_name in ("domain", "category", "tier", "complexity"):
        values = sorted(
            value
            for name, value in total_attributes
            if name == attribute_name
        )
        summary["distributions"][attribute_name] = {
            split: {
                value: split_attributes[split][(attribute_name, value)]
                for value in values
            }
            for split in SPLIT_RATIOS
        }
    return item_assignments, summary


def leakage_report(
    items: dict[str, dict[str, Any]],
    assignments: dict[str, dict[str, str]],
) -> dict[str, int]:
    exact_code_splits: dict[str, set[str]] = defaultdict(set)
    ast_splits: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    prompt_template_splits: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    family_splits: dict[str, set[str]] = defaultdict(set)
    for item_id, item in items.items():
        split = assignments[item_id]["split"]
        family_splits[assignments[item_id]["family_id"]].add(split)
        exact_code_splits[exact_code_hash(item["python_code"])].add(split)
        ast_splits[
            (item["domain"], item["category"], ast_template_hash(item["python_code"]))
        ].add(split)
        prompt_template_splits[
            (item["domain"], item["category"], normalized_prompt(item["prompt"]))
        ].add(split)
    return {
        "families_crossing_splits": sum(len(splits) > 1 for splits in family_splits.values()),
        "exact_code_groups_crossing_splits": sum(
            len(splits) > 1 for splits in exact_code_splits.values()
        ),
        "ast_template_groups_crossing_splits": sum(
            len(splits) > 1 for splits in ast_splits.values()
        ),
        "prompt_template_groups_crossing_splits": sum(
            len(splits) > 1 for splits in prompt_template_splits.values()
        ),
    }


def family_size_distribution(families: dict[str, list[str]]) -> dict[str, int]:
    buckets = Counter()
    for family in families.values():
        size = len(family)
        if size == 1:
            bucket = "1"
        elif size <= 3:
            bucket = "2-3"
        elif size <= 5:
            bucket = "4-5"
        elif size <= 10:
            bucket = "6-10"
        elif size <= 25:
            bucket = "11-25"
        elif size <= 50:
            bucket = "26-50"
        else:
            bucket = "51+"
        buckets[bucket] += 1
    return dict(buckets)


def markdown_report(report: dict[str, Any]) -> str:
    split_rows = "\n".join(
        f"| {split} | {report['splits']['item_counts'][split]} | "
        f"{report['splits']['family_counts'][split]} |"
        for split in SPLIT_RATIOS
    )
    size_rows = "\n".join(
        f"- `{bucket}` items: {count} familias"
        for bucket, count in report["families"]["size_distribution"].items()
    )
    edge_rows = "\n".join(
        f"- `{reason}`: {count} uniones"
        for reason, count in report["detection"]["edge_counts"].items()
    ) or "- Ninguna union."
    leakage_rows = "\n".join(
        f"- `{check}`: {count}"
        for check, count in report["leakage_checks"].items()
    )
    largest_rows = "\n".join(
        f"- `{family['family_id']}`: {family['size']} items, "
        f"{', '.join(family['item_ids'][:12])}"
        for family in report["families"]["largest"][:20]
    )
    examples = "\n".join(
        f"- `{pair['left']}` / `{pair['right']}`: "
        f"Jaccard={pair['jaccard']}, secuencia={pair['sequence']}"
        for pair in report["detection"]["prompt_similar_pairs"][:30]
    ) or "- No se detectaron pares aproximados."

    return f"""# Familias y propuesta de splits del dataset de creacion v1

Generado: `{report['created_at']}`

Dataset: `{report['dataset']['path']}`

SHA-256: `{report['dataset']['sha256']}`

## Metodo

- Codigo exactamente igual.
- Plantilla AST con nombres de variables y constantes normalizados.
- Prompt normalizado con numeros y unidades abstraidos.
- Similitud lexica dentro del mismo dominio y categoria.
- Jaccard minimo: {report['method']['prompt_jaccard_threshold']}.
- Similitud de secuencia minima: {report['method']['prompt_sequence_threshold']}.
- Seed de asignacion: {report['method']['seed']}.

La similitud lexica detecta parafrasis cercanas, pero no reemplaza una revision posterior
con embeddings semanticos. El manifiesto conserva metodo y umbrales para reproducibilidad.

## Familias

- Items: {report['families']['item_count']}
- Familias: {report['families']['family_count']}
- Familias singleton: {report['families']['singleton_count']}
- Familias con varios items: {report['families']['multi_item_count']}
- Familia mas grande: {report['families']['largest_size']} items

{size_rows}

## Evidencia de agrupacion

{edge_rows}

- Pares de prompts comparados: {report['detection']['prompt_pairs_compared']}
- Pares aproximados detectados: {report['detection']['prompt_similar_pair_count']}

## Propuesta de splits

| Split | Items | Familias |
|---|---:|---:|
{split_rows}

## Comprobaciones de fuga

{leakage_rows}

Todos estos valores deben ser cero antes de usar los splits para entrenamiento.

## Familias mas grandes

{largest_rows}

## Ejemplos de prompts similares

{examples}

## Estado

Esta es una propuesta reproducible. No modifica `dataset_creation_v1.json`. Antes de
congelarla se deben inspeccionar las familias grandes y validar una muestra de pares
aproximados para controlar falsos positivos y falsos negativos.
"""


def ensure_writable(paths: list[Path], force: bool) -> None:
    if force:
        return
    existing = [portable_path(path) for path in paths if path.exists()]
    if existing:
        raise FileExistsError(
            "Las salidas ya existen; usa --force para reemplazarlas: "
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


def main() -> None:
    args = parse_args()
    dataset_path = args.dataset.resolve()
    manifest_path = args.manifest.resolve()
    json_report_path = args.json_report.resolve()
    md_report_path = args.md_report.resolve()
    ensure_writable(
        [manifest_path, json_report_path, md_report_path],
        args.force,
    )

    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    items = dataset.get("items", {})
    if not isinstance(items, dict) or not items:
        raise ValueError("El dataset no contiene items validos")

    families, detection = detect_families(
        items,
        args.prompt_jaccard,
        args.prompt_sequence,
    )
    assignments, split_summary = propose_splits(families, items, args.seed)
    leakage = leakage_report(items, assignments)
    largest = sorted(
        (
            {
                "family_id": family_id,
                "size": len(item_ids),
                "item_ids": item_ids,
            }
            for family_id, item_ids in families.items()
        ),
        key=lambda value: (-value["size"], value["family_id"]),
    )

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "dataset": {
            "path": portable_path(dataset_path),
            "sha256": sha256_file(dataset_path),
            "version": dataset.get("meta", {}).get("dataset_version"),
        },
        "method": {
            "version": "family-split-v1.0.0",
            "signals": [
                "exact_code",
                "normalized_ast_template",
                "normalized_prompt_template",
                "strict_prompt_lexical_similarity",
            ],
            "prompt_jaccard_threshold": args.prompt_jaccard,
            "prompt_sequence_threshold": args.prompt_sequence,
            "seed": args.seed,
            "ratios": SPLIT_RATIOS,
            "embedding_validation": "pending",
        },
        "families": {
            "item_count": len(items),
            "family_count": len(families),
            "singleton_count": sum(len(family) == 1 for family in families.values()),
            "multi_item_count": sum(len(family) > 1 for family in families.values()),
            "largest_size": max(map(len, families.values())),
            "size_distribution": family_size_distribution(families),
            "largest": largest,
        },
        "detection": detection,
        "splits": split_summary,
        "leakage_checks": leakage,
    }

    manifest = {
        "created_at": report["created_at"],
        "version": "creation-splits-v1.0.0",
        "status": "proposal",
        "dataset": report["dataset"],
        "method": report["method"],
        "families": families,
        "assignments": assignments,
        "summary": split_summary,
        "leakage_checks": leakage,
    }

    write_json(json_report_path, report)
    write_json(manifest_path, manifest)
    md_report_path.parent.mkdir(parents=True, exist_ok=True)
    md_report_path.write_text(markdown_report(report), encoding="utf-8")

    print(f"Items: {len(items)}")
    print(f"Familias: {len(families)}")
    print(f"Familia maxima: {report['families']['largest_size']}")
    print(f"Splits: {split_summary['item_counts']}")
    print(f"Fugas detectadas: {sum(leakage.values())}")
    print(f"Reporte: {md_report_path}")
    print(f"Manifiesto propuesto: {manifest_path}")


if __name__ == "__main__":
    main()
