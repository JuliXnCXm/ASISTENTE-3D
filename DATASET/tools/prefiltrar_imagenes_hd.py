#!/usr/bin/env python3
"""
Pre-filtrado automático de imágenes arquitectónicas HD (Exterior e Interior)
para construcción de Dataset Sintético Gold-Standard (Qwen 7B LoRA / bpy).

Evalúa cada imagen en 6 ejes técnicos y arquitectónicos:
  1. Resolución mínima y relación de aspecto válida (sin banners ni recortes extremos).
  2. Nitidez (varianza del Laplaciano y energía de gradiente).
  3. Exposición y rango dinámico (descarta fotos quemadas, subexpuestas o planas).
  4. Señal geométrica arquitectónica (densidad de bordes verticales/horizontales/perspectiva).
  5. Control de oclusión vegetal (penaliza imágenes tapadas >78% por follaje).
  6. Deduplicación perceptual (dHash 64-bit) + Muestreo de Máxima Diversidad (Farthest-Point Sampling)
     para garantizar generalización cromática, lumínica y compositiva.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
import html
import json
import math
import os
import shutil
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
from PIL import Image, UnidentifiedImageError

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


@dataclass
class ImageAuditResult:
    filename: str
    source_path: str
    category: str
    status: str  # "selected" | "rejected"
    reason: str
    width: int = 0
    height: int = 0
    aspect_ratio: float = 0.0
    sharpness: float = 0.0
    mean_luminance: float = 0.0
    dynamic_range: float = 0.0
    arch_edge_score: float = 0.0
    green_occlusion: float = 0.0
    quality_score: float = 0.0
    dhash_hex: str = ""
    output_path: Optional[str] = None


def compute_dhash_64(gray_small_9x8: np.ndarray) -> int:
    """Calcula un hash perceptual dHash de 64 bits a partir de una matriz (8, 9)."""
    diff = gray_small_9x8[:, 1:] > gray_small_9x8[:, :-1]
    bits = diff.flatten()
    h = 0
    for b in bits:
        h = (h << 1) | int(bool(b))
    return h


def hamming_distance_64(h1: int, h2: int) -> int:
    return (h1 ^ h2).bit_count()


def evaluate_single_image(
    path: Path,
    category: str,
    min_resolution: int = 768,
    min_sharpness: float = 45.0,
    max_green_occlusion: float = 0.60,
) -> Tuple[ImageAuditResult, Optional[np.ndarray], Optional[int]]:
    """
    Analiza una imagen y devuelve (ImageAuditResult, feature_vector_24d, dhash_int).
    Si la imagen falla un filtro duro, status='rejected' y especifica el motivo.
    """
    try:
        with Image.open(path) as im:
            width, height = im.size
            min_side = min(width, height)
            aspect = round(width / max(1, height), 4)

            if min_side < min_resolution:
                return (
                    ImageAuditResult(
                        filename=path.name,
                        source_path=str(path),
                        category=category,
                        status="rejected",
                        reason=f"low_resolution ({width}x{height} < {min_resolution}px)",
                        width=width,
                        height=height,
                        aspect_ratio=aspect,
                    ),
                    None,
                    None,
                )

            if aspect < 0.42 or aspect > 2.55:
                return (
                    ImageAuditResult(
                        filename=path.name,
                        source_path=str(path),
                        category=category,
                        status="rejected",
                        reason=f"extreme_aspect_ratio ({aspect:.2f})",
                        width=width,
                        height=height,
                        aspect_ratio=aspect,
                    ),
                    None,
                    None,
                )

            # Aceleración DCT en JPEG grandes antes de decodificar píxeles
            try:
                im.draft("RGB", (512, 512))
            except Exception:
                pass
            rgb_im = im.convert("RGB")
            im_512 = rgb_im.resize((512, 512), Image.Resampling.BILINEAR)
    except (UnidentifiedImageError, OSError, ValueError, SyntaxError):
        return (
            ImageAuditResult(
                filename=path.name,
                source_path=str(path),
                category=category,
                status="rejected",
                reason="corrupt_or_unreadable",
            ),
            None,
            None,
        )
    arr = np.asarray(im_512, dtype=np.float32)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    gray = 0.299 * r + 0.587 * g + 0.114 * b

    # dHash 64-bit sobre 9x8
    gray_9x8 = np.asarray(
        im_512.convert("L").resize((9, 8), Image.Resampling.BILINEAR),
        dtype=np.float32,
    )
    dhash_val = compute_dhash_64(gray_9x8)
    dhash_hex = f"{dhash_val:016x}"

    # Exposición y rango dinámico
    mean_lum = float(np.mean(gray))
    p5, p95 = np.percentile(gray, [5, 95])
    dyn_range = float(p95 - p5)
    clipped_dark = float(np.mean(gray < 10.0))
    clipped_bright = float(np.mean(gray > 248.0))

    if mean_lum < 18.0 or clipped_dark > 0.65:
        return (
            ImageAuditResult(
                filename=path.name,
                source_path=str(path),
                category=category,
                status="rejected",
                reason=f"underexposed_dark (mean_lum={mean_lum:.1f})",
                width=width,
                height=height,
                aspect_ratio=aspect,
                mean_luminance=round(mean_lum, 2),
                dynamic_range=round(dyn_range, 2),
                dhash_hex=dhash_hex,
            ),
            None,
            None,
        )

    if mean_lum > 242.0 or clipped_bright > 0.50:
        return (
            ImageAuditResult(
                filename=path.name,
                source_path=str(path),
                category=category,
                status="rejected",
                reason=f"overexposed_burned (bright_clip={clipped_bright:.2f})",
                width=width,
                height=height,
                aspect_ratio=aspect,
                mean_luminance=round(mean_lum, 2),
                dynamic_range=round(dyn_range, 2),
                dhash_hex=dhash_hex,
            ),
            None,
            None,
        )

    if dyn_range < 32.0:
        return (
            ImageAuditResult(
                filename=path.name,
                source_path=str(path),
                category=category,
                status="rejected",
                reason=f"low_contrast_flat (dyn_range={dyn_range:.1f})",
                width=width,
                height=height,
                aspect_ratio=aspect,
                mean_luminance=round(mean_lum, 2),
                dynamic_range=round(dyn_range, 2),
                dhash_hex=dhash_hex,
            ),
            None,
            None,
        )

    # Nitidez (Varianza del Laplaciano discreto 2D)
    lap = (
        -4.0 * gray[1:-1, 1:-1]
        + gray[:-2, 1:-1]
        + gray[2:, 1:-1]
        + gray[1:-1, :-2]
        + gray[1:-1, 2:]
    )
    sharpness = float(np.var(lap))

    if sharpness < min_sharpness:
        return (
            ImageAuditResult(
                filename=path.name,
                source_path=str(path),
                category=category,
                status="rejected",
                reason=f"blurry_low_detail (sharpness={sharpness:.1f} < {min_sharpness})",
                width=width,
                height=height,
                aspect_ratio=aspect,
                sharpness=round(sharpness, 2),
                mean_luminance=round(mean_lum, 2),
                dynamic_range=round(dyn_range, 2),
                dhash_hex=dhash_hex,
            ),
            None,
            None,
        )

    # Señal geométrica arquitectónica (gradientes verticales y horizontales estructurados)
    gx = np.abs(gray[:, 2:] - gray[:, :-2])[1:-1, :]
    gy = np.abs(gray[2:, :] - gray[:-2, :])[:, 1:-1]
    strong_v = float(np.mean(gx > 22.0))
    strong_h = float(np.mean(gy > 22.0))
    arch_edge_score = float(min(100.0, (strong_v * 0.55 + strong_h * 0.45) * 450.0))

    if arch_edge_score < 4.0:
        return (
            ImageAuditResult(
                filename=path.name,
                source_path=str(path),
                category=category,
                status="rejected",
                reason=f"weak_architectural_geometry (edge_score={arch_edge_score:.1f})",
                width=width,
                height=height,
                aspect_ratio=aspect,
                sharpness=round(sharpness, 2),
                mean_luminance=round(mean_lum, 2),
                dynamic_range=round(dyn_range, 2),
                arch_edge_score=round(arch_edge_score, 2),
                dhash_hex=dhash_hex,
            ),
            None,
            None,
        )

    # Oclusión por follaje verde excesivo
    green_mask = (g > r * 1.15) & (g > b * 1.20) & (g > 35.0)
    green_occ = float(np.mean(green_mask))
    if green_occ > max_green_occlusion:
        return (
            ImageAuditResult(
                filename=path.name,
                source_path=str(path),
                category=category,
                status="rejected",
                reason=f"excessive_foliage_occlusion ({green_occ*100:.0f}% green)",
                width=width,
                height=height,
                aspect_ratio=aspect,
                sharpness=round(sharpness, 2),
                mean_luminance=round(mean_lum, 2),
                dynamic_range=round(dyn_range, 2),
                arch_edge_score=round(arch_edge_score, 2),
                green_occlusion=round(green_occ, 3),
                dhash_hex=dhash_hex,
            ),
            None,
            None,
        )

    # Puntaje compuesto de calidad arquitectónica (0..100)
    res_bonus = min(25.0, (min_side / 1500.0) * 25.0)
    sharp_score = min(30.0, (math.log1p(sharpness) / math.log1p(1200.0)) * 30.0) if False else min(30.0, float(np.log1p(sharpness) / np.log1p(1200.0)) * 30.0)
    dyn_score = min(20.0, (dyn_range / 180.0) * 20.0)
    edge_bonus = min(25.0, (arch_edge_score / 45.0) * 25.0)
    foliage_penalty = max(0.0, (green_occ - 0.45) * 25.0)

    quality_score = round(res_bonus + sharp_score + dyn_score + edge_bonus - foliage_penalty, 2)

    # Vector descriptor de 24 dimensiones para muestreo de máxima diversidad (color 3x3 + iluminación + orientación de bordes)
    small_3x3 = np.asarray(im_512.resize((3, 3), Image.Resampling.BOX), dtype=np.float32) / 255.0
    feat_color = small_3x3.reshape(-1)[:18]  # 18 dims
    warmth = float(np.mean(r - b) / 255.0)
    feat_extra = np.array(
        [
            mean_lum / 255.0,
            dyn_range / 255.0,
            warmth,
            strong_v,
            strong_h,
            aspect / 2.0,
        ],
        dtype=np.float32,
    )
    feature_vec = np.concatenate([feat_color, feat_extra])

    return (
        ImageAuditResult(
            filename=path.name,
            source_path=str(path),
            category=category,
            status="candidate",
            reason="passed_technical_filters",
            width=width,
            height=height,
            aspect_ratio=aspect,
            sharpness=round(sharpness, 2),
            mean_luminance=round(mean_lum, 2),
            dynamic_range=round(dyn_range, 2),
            arch_edge_score=round(arch_edge_score, 2),
            green_occlusion=round(green_occ, 3),
            quality_score=quality_score,
            dhash_hex=dhash_hex,
        ),
        feature_vec,
        dhash_val,
    )


def deduplicate_and_diversify(
    records: List[Tuple[ImageAuditResult, Optional[np.ndarray], Optional[int]]],
    max_select: int,
    hash_threshold: int = 6,
) -> List[ImageAuditResult]:
    """
    1. Ordena candidatos válidos por quality_score descendente.
    2. Elimina duplicados perceptuales (dHash Hamming <= hash_threshold).
    3. Si sobran candidatos respecto a max_select, aplica Farthest-Point Sampling
       ponderado por calidad para maximizar diversidad visual y generalización.
    """
    rejected: List[ImageAuditResult] = []
    valid: List[Tuple[ImageAuditResult, np.ndarray, int]] = []

    for res, feat, dhash in records:
        if res.status != "candidate" or feat is None or dhash is None:
            rejected.append(res)
        else:
            valid.append((res, feat, dhash))

    # Ordenar por calidad descendente para que al deduplicar quede siempre la mejor versión
    valid.sort(key=lambda item: (item[0].quality_score, item[0].width * item[0].height, item[0].filename), reverse=True)

    unique_valid: List[Tuple[ImageAuditResult, np.ndarray]] = []
    accepted_hashes: List[Tuple[int, np.ndarray, str]] = []

    for res, feat, dhash in valid:
        dup_of = None
        for prev_hash, prev_feat, prev_name in accepted_hashes:
            if hamming_distance_64(dhash, prev_hash) <= hash_threshold:
                color_diff = float(np.mean(np.abs(feat[:18] - prev_feat[:18])))
                if color_diff < 0.05:
                    dup_of = prev_name
                    break
        if dup_of is not None:
            res.status = "rejected"
            res.reason = f"near_duplicate_of ({dup_of})"
            rejected.append(res)
        else:
            accepted_hashes.append((dhash, feat, res.filename))
            unique_valid.append((res, feat))

    if len(unique_valid) <= max_select:
        selected = []
        for res, _ in unique_valid:
            res.status = "selected"
            res.reason = "selected_high_quality_unique"
            selected.append(res)
        return selected + rejected

    # Farthest-Point Sampling ponderado por quality_score para máxima diversidad
    chosen_indices = [0]  # Empezamos por la imagen de mayor puntaje
    feats = np.stack([f for _, f in unique_valid], axis=0)
    qualities = np.array([r.quality_score for r, _ in unique_valid], dtype=np.float32)
    q_norm = (qualities - qualities.min()) / max(1e-5, (qualities.max() - qualities.min()))

    min_dists = np.linalg.norm(feats - feats[0], axis=1)
    min_dists[0] = -1.0

    while len(chosen_indices) < max_select:
        # Combinar distancia al conjunto ya elegido (70%) + calidad intrínseca (30%)
        d_max = max(1e-5, float(min_dists.max()))
        combined = 0.70 * (min_dists / d_max) + 0.30 * q_norm
        combined[chosen_indices] = -1.0
        next_idx = int(np.argmax(combined))
        chosen_indices.append(next_idx)
        new_dists = np.linalg.norm(feats - feats[next_idx], axis=1)
        min_dists = np.minimum(min_dists, new_dists)

    chosen_set = set(chosen_indices)
    final_results: List[ImageAuditResult] = []
    for idx, (res, _) in enumerate(unique_valid):
        if idx in chosen_set:
            res.status = "selected"
            res.reason = "selected_diverse_high_quality"
            final_results.append(res)
        else:
            res.status = "rejected"
            res.reason = "quota_exceeded_lower_diversity"
            rejected.append(res)

    return final_results + rejected


def write_html_gallery(output_dir: Path, results: List[ImageAuditResult], summary: Dict) -> Path:
    html_path = output_dir / "galeria_prefiltrado.html"
    selected = [r for r in results if r.status == "selected"]
    rejected = [r for r in results if r.status == "rejected"]

    cards_sel = []
    for r in selected:
        rel_img = os.path.relpath(r.output_path or r.source_path, output_dir)
        cards_sel.append(
            f"""
            <div class="card selected">
              <img src="{html.escape(rel_img)}" loading="lazy" alt="{html.escape(r.filename)}"/>
              <div class="meta">
                <strong>[{html.escape(r.category.upper())}] {html.escape(r.filename)}</strong>
                <span>Score: <b>{r.quality_score}</b> | {r.width}×{r.height}</span>
                <span>Sharpness: {r.sharpness} | ArchEdge: {r.arch_edge_score}</span>
              </div>
            </div>
            """
        )

    rows_rej = []
    for r in rejected[:250]:
        rows_rej.append(
            f"<tr><td>{html.escape(r.category)}</td><td>{html.escape(r.filename)}</td>"
            f"<td>{r.width}×{r.height}</td><td>{html.escape(r.reason)}</td></tr>"
        )

    doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8"/>
<title>Galería de Pre-Filtrado Arquitectónico HD</title>
<style>
  body {{ font-family: system-ui, sans-serif; background: #121518; color: #e4e8ec; margin: 24px; }}
  h1, h2 {{ color: #f5f7fa; }}
  .summary {{ background: #1c2127; padding: 16px; border-radius: 8px; margin-bottom: 24px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }}
  .card {{ background: #1c2127; border: 1px solid #2e3640; border-radius: 8px; overflow: hidden; }}
  .card img {{ width: 100%; height: 190px; object-fit: cover; display: block; }}
  .meta {{ padding: 10px; font-size: 13px; display: flex; flex-direction: column; gap: 4px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 13px; }}
  th, td {{ border-bottom: 1px solid #2e3640; padding: 8px; text-align: left; }}
</style>
</head>
<body>
  <h1>Reporte Visual de Pre-Filtrado (Dataset Sintético Qwen 7B LoRA)</h1>
  <div class="summary">
    <p><b>Exterior:</b> {summary['exterior']['selected']} seleccionadas / {summary['exterior']['rejected']} descartadas (Total: {summary['exterior']['total']})</p>
    <p><b>Interior:</b> {summary['interior']['selected']} seleccionadas / {summary['interior']['rejected']} descartadas (Total: {summary['interior']['total']})</p>
  </div>
  <h2>Imágenes Seleccionadas ({len(selected)})</h2>
  <div class="grid">{''.join(cards_sel)}</div>
  <h2>Imágenes Descartadas ({len(rejected)})</h2>
  <table>
    <thead><tr><th>Categoría</th><th>Archivo</th><th>Resolución</th><th>Motivo de Descarte</th></tr></thead>
    <tbody>{''.join(rows_rej)}</tbody>
  </table>
</body>
</html>"""
    html_path.write_text(doc, encoding="utf-8")
    return html_path


def _eval_worker(task_tuple):
    p, category, min_res, min_sharp, max_green = task_tuple
    return evaluate_single_image(
        p,
        category=category,
        min_resolution=min_res,
        min_sharpness=min_sharp,
        max_green_occlusion=max_green,
    )


def _scan_image_files(input_dir: Path) -> List[Path]:
    found: List[Path] = []
    stack = [input_dir]
    while stack:
        curr = stack.pop()
        try:
            with os.scandir(curr) as it:
                for entry in it:
                    if entry.is_dir(follow_symlinks=False):
                        stack.append(Path(entry.path))
                    elif entry.is_file(follow_symlinks=False):
                        ext = os.path.splitext(entry.name)[1].lower()
                        if ext in VALID_EXTENSIONS:
                            found.append(Path(entry.path))
        except OSError:
            continue
    found.sort()
    return found


def process_category_folder(
    input_dir: Optional[Path],
    output_cat_dir: Path,
    category: str,
    min_resolution: int,
    min_sharpness: float,
    max_green_occlusion: float,
    max_select: int,
    hash_threshold: int,
    use_symlink: bool,
    workers: int = 1,
) -> List[ImageAuditResult]:
    if input_dir is None or not input_dir.exists():
        return []

    output_cat_dir.mkdir(parents=True, exist_ok=True)
    files = _scan_image_files(input_dir)

    if workers > 1 and len(files) >= 64:
        tasks = [
            (p, category, min_resolution, min_sharpness, max_green_occlusion)
            for p in files
        ]
        with ProcessPoolExecutor(max_workers=workers) as pool:
            evaluated = list(pool.map(_eval_worker, tasks, chunksize=64))
    else:
        evaluated = [
            evaluate_single_image(
                p,
                category=category,
                min_resolution=min_resolution,
                min_sharpness=min_sharpness,
                max_green_occlusion=max_green_occlusion,
            )
            for p in files
        ]

    curated = deduplicate_and_diversify(
        evaluated, max_select=max_select, hash_threshold=hash_threshold
    )

    for rank, item in enumerate(
        sorted([c for c in curated if c.status == "selected"], key=lambda x: x.quality_score, reverse=True),
        start=1,
    ):
        src = Path(item.source_path)
        dst_name = f"{category[:3]}_{rank:04d}_{src.name}"
        dst = output_cat_dir / dst_name
        if dst.exists():
            dst.unlink()
        if use_symlink:
            dst.symlink_to(src.resolve())
        else:
            shutil.copy2(src, dst)
        item.output_path = str(dst)

    return curated


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pre-filtra imágenes HD de exterior e interior por nitidez, geometría arquitectónica y diversidad."
    )
    parser.add_argument("--exterior-dir", type=Path, required=True, help="Carpeta con imágenes de exterior.")
    parser.add_argument("--interior-dir", type=Path, required=True, help="Carpeta con imágenes de interior.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Carpeta destino para las imágenes curadas y el reporte.")
    parser.add_argument("--min-resolution", type=int, default=768, help="Lado mínimo permitido en píxeles (default: 768).")
    parser.add_argument("--min-sharpness", type=float, default=45.0, help="Varianza mínima del Laplaciano para descartar fotos borrosas (default: 45.0).")
    parser.add_argument("--max-green-occlusion", type=float, default=0.60, help="Fracción máxima de follaje verde permitida (default: 0.60).")
    parser.add_argument("--max-exterior", type=int, default=600, help="Cupo máximo de imágenes de exterior diversas a seleccionar (default: 600).")
    parser.add_argument("--max-interior", type=int, default=280, help="Cupo máximo de imágenes de interior diversas a seleccionar (default: 280).")
    parser.add_argument("--hash-threshold", type=int, default=6, help="Umbral de distancia Hamming dHash para detectar duplicados (default: 6).")
    parser.add_argument("--workers", type=int, default=max(1, min(20, os.cpu_count() or 4)), help="Procesos en paralelo (default: auto).")
    parser.add_argument("--symlink", action="store_true", help="Crear symlinks en lugar de copiar los archivos seleccionados.")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    ext_results = process_category_folder(
        input_dir=args.exterior_dir,
        output_cat_dir=args.output_dir / "exterior",
        category="exterior",
        min_resolution=args.min_resolution,
        min_sharpness=args.min_sharpness,
        max_green_occlusion=args.max_green_occlusion,
        max_select=args.max_exterior,
        hash_threshold=args.hash_threshold,
        use_symlink=args.symlink,
        workers=args.workers,
    )

    int_results = process_category_folder(
        input_dir=args.interior_dir,
        output_cat_dir=args.output_dir / "interior",
        category="interior",
        min_resolution=args.min_resolution,
        min_sharpness=args.min_sharpness,
        max_green_occlusion=min(0.90, args.max_green_occlusion + 0.10),
        max_select=args.max_interior,
        hash_threshold=args.hash_threshold,
        use_symlink=args.symlink,
        workers=args.workers,
    )

    all_results = ext_results + int_results
    reason_counts = dict(Counter(r.reason.split(" (")[0] for r in all_results))
    summary = {
        "exterior": {
            "total": len(ext_results),
            "selected": sum(1 for r in ext_results if r.status == "selected"),
            "rejected": sum(1 for r in ext_results if r.status == "rejected"),
        },
        "interior": {
            "total": len(int_results),
            "selected": sum(1 for r in int_results if r.status == "selected"),
            "rejected": sum(1 for r in int_results if r.status == "rejected"),
        },
        "reasons_breakdown": reason_counts,
    }

    selected_items = [asdict(r) for r in all_results if r.status == "selected"]
    rejected_items = [asdict(r) for r in all_results if r.status == "rejected"]
    # Si hay más de 2000 rechazadas, guardar las seleccionadas completas + muestra de 500 rechazadas para mantener el JSON ágil
    items_for_json = selected_items + (rejected_items if len(rejected_items) <= 2000 else rejected_items[:500])

    report_payload = {
        "summary": summary,
        "parameters": {
            "min_resolution": args.min_resolution,
            "min_sharpness": args.min_sharpness,
            "max_green_occlusion": args.max_green_occlusion,
            "max_exterior": args.max_exterior,
            "max_interior": args.max_interior,
            "hash_threshold": args.hash_threshold,
        },
        "items": items_for_json,
    }

    report_path = args.output_dir / "reporte_prefiltrado.json"
    report_path.write_text(json.dumps(report_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    gallery_path = write_html_gallery(args.output_dir, all_results, summary)

    print("=== Resumen de Pre-Filtrado Arquitectónico HD ===")
    print(
        f"Exterior: {summary['exterior']['selected']} seleccionadas / "
        f"{summary['exterior']['rejected']} descartadas (Total analizadas: {summary['exterior']['total']})"
    )
    print(
        f"Interior: {summary['interior']['selected']} seleccionadas / "
        f"{summary['interior']['rejected']} descartadas (Total analizadas: {summary['interior']['total']})"
    )
    print(f"Reporte JSON: {report_path}")
    print(f"Galería HTML: {gallery_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
