import json
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "DATASET" / "tools" / "prefiltrar_imagenes_hd.py"


def _make_architectural_image(path: Path, width=1024, height=1024, seed=0, tint=(180, 195, 210)):
    rng = np.random.default_rng(seed)
    img = Image.new("RGB", (width, height), color=tint)
    draw = ImageDraw.Draw(img)
    # Draw crisp architectural vertical columns, horizontal slabs, and diagonal perspective lines
    for x in range(80, width - 80, 110):
        draw.rectangle([x, 120, x + 24, height - 100], fill=(45, 50, 58), outline=(240, 240, 245))
    for y in range(140, height - 120, 130):
        draw.rectangle([60, y, width - 60, y + 18], fill=(85, 65, 45), outline=(220, 210, 195))
    draw.line([(0, height), (width // 2, height // 3), (width, height)], fill=(255, 210, 130), width=5)
    # Add subtle micro-texture so entropy and dynamic range are realistic
    arr = np.asarray(img, dtype=np.int16)
    noise = rng.integers(-12, 13, size=arr.shape, dtype=np.int16)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    Image.fromarray(arr, mode="RGB").save(path)


def _make_blurry_or_dark_image(path: Path, width=1024, height=1024, dark=False):
    val = 8 if dark else 128
    arr = np.full((height, width, 3), val, dtype=np.uint8)
    Image.fromarray(arr, mode="RGB").save(path)


def test_cli_prefiltrado_filters_duplicates_blurry_and_generates_report(tmp_path: Path):
    ext_dir = tmp_path / "raw_exterior"
    int_dir = tmp_path / "raw_interior"
    out_dir = tmp_path / "curated_out"
    ext_dir.mkdir()
    int_dir.mkdir()

    # 1. Valid diverse exterior images
    _make_architectural_image(ext_dir / "ext_good_01.png", seed=1, tint=(170, 195, 220))
    _make_architectural_image(ext_dir / "ext_good_02.png", seed=2, tint=(210, 175, 145))
    # Exact duplicate of ext_good_01
    _make_architectural_image(ext_dir / "ext_dup_01.png", seed=1, tint=(170, 195, 220))
    # Blurry flat image
    _make_blurry_or_dark_image(ext_dir / "ext_blurry.png", dark=False)
    # Too small resolution image
    _make_architectural_image(ext_dir / "ext_small.png", width=320, height=240, seed=3)
    # Corrupt file
    (ext_dir / "ext_corrupt.png").write_bytes(b"not_an_image_content")

    # 2. Valid interior images
    _make_architectural_image(int_dir / "int_good_01.jpg", seed=10, tint=(205, 190, 170))
    _make_blurry_or_dark_image(int_dir / "int_dark.jpg", dark=True)

    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--exterior-dir",
            str(ext_dir),
            "--interior-dir",
            str(int_dir),
            "--output-dir",
            str(out_dir),
            "--min-resolution",
            "768",
            "--max-exterior",
            "10",
            "--max-interior",
            "10",
        ],
        capture_output=True,
        text=True,
    )

    assert proc.returncode == 0, f"STDERR: {proc.stderr}\nSTDOUT: {proc.stdout}"
    assert "Resumen de Pre-Filtrado" in proc.stdout

    report_file = out_dir / "reporte_prefiltrado.json"
    gallery_file = out_dir / "galeria_prefiltrado.html"
    assert report_file.is_file()
    assert gallery_file.is_file()

    report = json.loads(report_file.read_text(encoding="utf-8"))
    assert report["summary"]["exterior"]["selected"] == 2
    assert report["summary"]["exterior"]["rejected"] == 4
    assert report["summary"]["interior"]["selected"] == 1
    assert report["summary"]["interior"]["rejected"] == 1

    selected_ext = list((out_dir / "exterior").glob("*"))
    selected_int = list((out_dir / "interior").glob("*"))
    assert len(selected_ext) == 2
    assert len(selected_int) == 1

    # Verify original input files were never deleted or modified
    assert len(list(ext_dir.iterdir())) == 6
    assert len(list(int_dir.iterdir())) == 2


def test_cli_prefiltrado_rejects_excess_foliage_and_enforces_diversity_quota(tmp_path: Path):
    ext_dir = tmp_path / "raw_ext_quota"
    int_dir = tmp_path / "raw_int_quota"
    out_dir = tmp_path / "curated_quota"
    ext_dir.mkdir()
    int_dir.mkdir()

    # Create 4 distinct valid exterior images + 1 pure-green foliage-occluded image
    for idx, tint in enumerate([(165, 190, 220), (215, 180, 140), (140, 160, 195), (225, 205, 175)]):
        _make_architectural_image(ext_dir / f"ext_valid_{idx}.png", seed=100 + idx, tint=tint)

    # Pure green image (>85% green pixels, with sharp grid lines so it passes sharpness)
    _make_architectural_image(ext_dir / "ext_pure_foliage.png", seed=999, tint=(30, 190, 40))

    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--exterior-dir",
            str(ext_dir),
            "--interior-dir",
            str(int_dir),
            "--output-dir",
            str(out_dir),
            "--max-exterior",
            "2",
            "--max-interior",
            "2",
        ],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    report = json.loads((out_dir / "reporte_prefiltrado.json").read_text(encoding="utf-8"))
    assert report["summary"]["exterior"]["selected"] == 2
    assert report["summary"]["exterior"]["rejected"] == 3
    reasons = {item["filename"]: item["reason"] for item in report["items"]}
    assert "excessive_foliage_occlusion" in reasons["ext_pure_foliage.png"]
    assert sum(1 for r in reasons.values() if r == "quota_exceeded_lower_diversity") == 2

