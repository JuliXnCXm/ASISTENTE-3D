#!/usr/bin/env python3
"""
Empaqueta el Dataset Gold-Standard (6 Categorías: Creación + Edición en Exterior, Interior y AEC)
con splits sin fugas por scene_id (train / validation / test), copia imágenes de referencia,
scripts .py y archivos .blend validados, genera el Dataset Card (README.md) y lo sube a Hugging Face Hub.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional
from PIL import Image


def assign_split_by_scene_id(scene_id: str, val_ratio: float = 0.10, test_ratio: float = 0.05) -> str:
    """Asigna todas las variantes de un mismo scene_id al mismo split para garantizar 0% data leakage."""
    h = int(hashlib.md5(scene_id.encode("utf-8")).hexdigest()[:8], 16) / float(0xFFFFFFFF)
    if h < test_ratio:
        return "test"
    if h < test_ratio + val_ratio:
        return "validation"
    return "train"


def _save_optimized_training_image(src_img: Path, dst_img: Path, max_side: int = 1280) -> None:
    dst_img.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src_img) as im:
        try:
            im.draft("RGB", (max_side, max_side))
        except Exception:
            pass
        rgb = im.convert("RGB")
        w, h = rgb.size
        if max(w, h) > max_side:
            scale = max_side / float(max(w, h))
            rgb = rgb.resize((int(w * scale), int(h * scale)), Image.Resampling.BILINEAR)
        rgb.save(dst_img, format="JPEG", quality=92, optimize=True)


def build_hf_package(
    input_jsonl: Path,
    export_dir: Path,
    repo_id: str,
    copy_assets: bool = True,
    sync_training_data_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    export_dir.mkdir(parents=True, exist_ok=True)
    splits: Dict[str, List[Dict[str, Any]]] = {"train": [], "validation": [], "test": []}
    cat_counter: Counter = Counter()

    records = [
        json.loads(line)
        for line in input_jsonl.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    for rec in records:
        sid = rec["scene_id"]
        sp = assign_split_by_scene_id(sid)
        rec_copy = dict(rec)
        rec_copy["split"] = sp

        if copy_assets:
            if rec_copy.get("image") and Path(rec_copy["image"]).is_file():
                src_img = Path(rec_copy["image"]).resolve()
                dst_img = export_dir / "images" / f"{sid}.jpg"
                if not dst_img.exists():
                    _save_optimized_training_image(src_img, dst_img, max_side=1280)
                rec_copy["image"] = f"images/{dst_img.name}"
                rec_copy["multimodal"] = {"image": f"images/{dst_img.name}"}
            elif rec_copy.get("image") is None:
                rec_copy["multimodal"] = {"image": None}

            if rec_copy.get("blend_path") and Path(rec_copy["blend_path"]).is_file():
                src_blend = Path(rec_copy["blend_path"]).resolve()
                dst_blend = export_dir / "blends" / src_blend.name
                dst_blend.parent.mkdir(parents=True, exist_ok=True)
                if not dst_blend.exists():
                    shutil.copy2(src_blend, dst_blend)
                rec_copy["blend_path"] = f"blends/{dst_blend.name}"

        splits[sp].append(rec_copy)
        cat_counter[rec_copy["matrix_category"]] += 1

    data_dir = export_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    for sp_name, sp_records in splits.items():
        out_f = data_dir / f"{sp_name}.jsonl"
        with out_f.open("w", encoding="utf-8") as f:
            for r in sp_records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

        if sync_training_data_dir is not None:
            sync_training_data_dir.mkdir(parents=True, exist_ok=True)
            train_target = sync_training_data_dir / f"{sp_name}_multimodal.jsonl"
            shutil.copy2(out_f, train_target)

    readme = f"""---
license: apache-2.0
task_categories:
  - image-to-text
  - text-generation
language:
  - es
tags:
  - blender
  - bpy
  - aec
  - bim
  - architecture
  - 3d-generation
  - qwen2.5-vl
---

# {repo_id} — Gold-Standard Multimodal Blender `bpy` & AEC Structural Dataset

Dataset multimodal (Imagen + Texto + Código `bpy` + Archivos `.blend` validados) con **Spatial Chain-of-Thought (`<plan_arquitectonico>` / `<plan_edicion>`)** y contrato de cierre **360° (6 caras)**.

## Resumen de Splits (Sin fuga de datos por `scene_id`)
- **Train:** `{len(splits['train'])}` muestras
- **Validation:** `{len(splits['validation'])}` muestras
- **Test:** `{len(splits['test'])}` muestras
- **Total:** `{len(records)}` muestras

## Distribución por Matriz de 6 Categorías
{json.dumps(dict(cat_counter), indent=2, ensure_ascii=False)}
"""
    (export_dir / "README.md").write_text(readme, encoding="utf-8")
    return {
        "total": len(records),
        "splits": {k: len(v) for k, v in splits.items()},
        "categories": dict(cat_counter),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Empaqueta y sube el dataset Gold-Standard a Hugging Face Hub.")
    parser.add_argument("--input-jsonl", type=Path, required=True, help="Archivo JSONL generado por generar_dataset_gold.py.")
    parser.add_argument("--export-dir", type=Path, required=True, help="Carpeta local donde armar el paquete Hugging Face.")
    parser.add_argument("--repo-id", type=str, default="julianG99/aec-procedural-blender-gold-v2", help="ID del repositorio en Hugging Face.")
    parser.add_argument(
        "--sync-training-dir",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "TRAINING" / "data",
        help="Sincroniza train_multimodal.jsonl / validation_multimodal.jsonl / test_multimodal.jsonl.",
    )
    parser.add_argument("--push-to-hub", action="store_true", help="Subir automáticamente a Hugging Face Hub usando HF_TOKEN.")
    args = parser.parse_args()

    stats = build_hf_package(
        args.input_jsonl,
        args.export_dir,
        args.repo_id,
        sync_training_data_dir=args.sync_training_dir,
    )
    print("=== Paquete Hugging Face Preparado ===")
    print(json.dumps(stats, indent=2, ensure_ascii=False))

    if args.push_to_hub:
        from huggingface_hub import HfApi

        api = HfApi(token=os.environ.get("HF_TOKEN"))
        api.create_repo(repo_id=args.repo_id, repo_type="dataset", exist_ok=True)
        api.upload_folder(
            folder_path=str(args.export_dir),
            repo_id=args.repo_id,
            repo_type="dataset",
        )
        print(f"Subido exitosamente a https://huggingface.co/datasets/{args.repo_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
