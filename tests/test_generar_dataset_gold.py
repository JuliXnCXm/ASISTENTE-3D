import ast
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "DATASET" / "scripts" / "generar_dataset_gold.py"


def _create_sample_curated_dir(base_dir: Path) -> Path:
    ext_dir = base_dir / "exterior"
    int_dir = base_dir / "interior"
    ext_dir.mkdir(parents=True)
    int_dir.mkdir(parents=True)

    for cat_dir, prefix, tint in [
        (ext_dir, "ext_0001_sample.jpg", (165, 205, 215)),
        (int_dir, "int_0001_sample.jpg", (210, 185, 150)),
    ]:
        img = Image.new("RGB", (1024, 1280), color=tint)
        draw = ImageDraw.Draw(img)
        draw.rectangle([120, 180, 900, 1050], fill=(80, 85, 92), outline=(240, 240, 240))
        draw.rectangle([220, 300, 500, 920], fill=(140, 95, 55), outline=(30, 30, 30))
        img.save(cat_dir / prefix)

    return base_dir


def test_generar_dataset_gold_creates_all_6_matrix_categories_with_valid_ast(tmp_path: Path):
    curated_dir = _create_sample_curated_dir(tmp_path / "curated")
    out_jsonl = tmp_path / "out" / "gold_train.jsonl"
    out_scripts = tmp_path / "out" / "scripts_bpy"
    out_blends = tmp_path / "out" / "blends"

    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--curated-dir",
            str(curated_dir),
            "--output-jsonl",
            str(out_jsonl),
            "--scripts-dir",
            str(out_scripts),
            "--blends-dir",
            str(out_blends),
            "--limit-exterior",
            "1",
            "--limit-interior",
            "1",
        ],
        capture_output=True,
        text=True,
    )

    assert proc.returncode == 0, f"STDERR: {proc.stderr}\nSTDOUT: {proc.stdout}"
    assert out_jsonl.is_file()
    assert out_blends.is_dir()

    lines = [json.loads(line) for line in out_jsonl.read_text(encoding="utf-8").splitlines() if line.strip()]
    # Verify all 6 matrix categories are generated across the exterior + interior scenes
    matrix_categories = {rec["matrix_category"] for rec in lines}
    assert matrix_categories == {
        "exterior_creation",
        "exterior_edit",
        "interior_creation",
        "interior_edit",
        "aec_structural_creation",
        "aec_structural_edit",
    }

    # Verify modality dropout variants exist
    variants_seen = {rec["variant"] for rec in lines}
    assert {
        "image_plus_prompt",
        "image_only",
        "text_only",
        "surgical_edit",
        "aec_structural_creation",
        "aec_structural_edit",
    }.issubset(variants_seen)

    for rec in lines:
        assert "blend_path" in rec
        assert rec["blend_path"].endswith(".blend")
        user_msg = rec["messages"][1]["content"]
        assistant_msg = rec["messages"][-1]["content"]

        # Verify explicit LOD and 360-closure conditioning tokens in user prompt
        assert "[NIVEL_DISENO: LOD_" in user_msg
        assert "[CIERRE: 360_6_CARAS]" in user_msg

        if rec["operation"] == "creation":
            assert "<plan_arquitectonico>" in assistant_msg
            assert "</plan_arquitectonico>" in assistant_msg
            plan_str = assistant_msg.split("<plan_arquitectonico>\n", 1)[1].split("\n</plan_arquitectonico>", 1)[0]
        else:
            assert rec["operation"] == "edit"
            assert "<plan_edicion>" in assistant_msg
            assert "</plan_edicion>" in assistant_msg
            plan_str = assistant_msg.split("<plan_edicion>\n", 1)[1].split("\n</plan_edicion>", 1)[0]

        plan_data = json.loads(plan_str)
        assert plan_data["nivel_diseno"] in {
            "LOD_500_ULTRA_DETALLE",
            "LOD_400_INGENIERIA_AEC",
            "LOD_350_ARQUITECTURA_360",
        }
        assert plan_data.get("validacion_6_caras_ok") is True
        cierre = plan_data.get("cierre_6_caras", {})
        assert set(cierre.keys()) == {
            "cara_1_frente_sur",
            "cara_2_contrafrente_norte",
            "cara_3_lateral_oeste_izq",
            "cara_4_lateral_este_der",
            "cara_5_base_suelo",
            "cara_6_cubierta_techo",
        }
        assert all(isinstance(v, str) and len(v) > 10 for v in cierre.values())

        assert "```python" in assistant_msg
        code_block = assistant_msg.split("```python\n", 1)[1].split("```", 1)[0]
        ast.parse(code_block)
        assert "import bpy" in code_block
        assert "import bmesh" in code_block
        assert "ShaderNodeBsdfPrincipled" in code_block

        if rec["operation"] == "edit":
            # Surgical edit scripts must check existing objects idempotently before replacing/adding
            assert "bpy.data.objects.get" in code_block

    # Running a second time with --resume must skip already completed scenes without duplicating lines
    proc2 = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--curated-dir",
            str(curated_dir),
            "--output-jsonl",
            str(out_jsonl),
            "--scripts-dir",
            str(out_scripts),
            "--blends-dir",
            str(out_blends),
            "--limit-exterior",
            "1",
            "--limit-interior",
            "1",
            "--api-workers",
            "2",
            "--resume",
        ],
        capture_output=True,
        text=True,
    )
    assert proc2.returncode == 0, proc2.stderr
    lines_after = [json.loads(line) for line in out_jsonl.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(lines_after) == len(lines)

