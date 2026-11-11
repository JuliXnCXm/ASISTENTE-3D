import json
from pathlib import Path
import sys

INFERENCE_DIR = Path(__file__).resolve().parents[1] / "INFERENCE"
sys.path.insert(0, str(INFERENCE_DIR))


def test_bridge_agent_qwen_formats_3_modalities_and_auto_corrects_bridge_errors(tmp_path: Path):
    import bridge_agent_qwen as baq

    # 1. Verify prompt formatting for all 3 modalities + edit mode
    msg_text_only = baq.build_user_instruction(
        prompt="Diseña una casa en lote de 250 m2",
        image_path=None,
        lod="LOD_500_ULTRA_DETALLE",
        operation="creation",
        scene_info=None,
    )
    assert "[NIVEL_DISENO: LOD_500_ULTRA_DETALLE]" in msg_text_only
    assert "[CIERRE: 360_6_CARAS]" in msg_text_only
    assert "<image>" not in msg_text_only

    msg_img_only = baq.build_user_instruction(
        prompt="",
        image_path=tmp_path / "foto.jpg",
        lod="LOD_500_ULTRA_DETALLE",
        operation="creation",
        scene_info=None,
    )
    assert msg_img_only.startswith("<image>\n")
    assert "Reconstruye esta escena" in msg_img_only

    msg_edit = baq.build_user_instruction(
        prompt="Completa la escalera y agrega puerta de 2m",
        image_path=tmp_path / "foto.jpg",
        lod="LOD_500_ULTRA_DETALLE",
        operation="edit",
        scene_info={"object_count": 120, "objects": [{"name": "Muro_Sur"}]},
    )
    assert "<escena_actual_blender>" in msg_edit
    assert "Muro_Sur" in msg_edit

    # 2. Verify execution + auto-correction loop against a simulated Bridge + Model
    model_calls = []

    def fake_model_generate(messages, image_path=None):
        model_calls.append(messages)
        if len(model_calls) == 1:
            # First attempt returns broken syntax
            return "<plan_arquitectonico>\n{\"cierre_6_caras\": {}}\n</plan_arquitectonico>\n```python\nimport bpy\nbpy.ops.broken(\n```"
        # Second attempt after receiving traceback fixes the code
        return "<plan_arquitectonico>\n{\"cierre_6_caras\": {}}\n</plan_arquitectonico>\n```python\nimport bpy\nimport bmesh\n```"

    bridge_calls = []

    def fake_bridge_rpc(method, params, bridge_url="http://127.0.0.1:8765/rpc"):
        bridge_calls.append((method, params))
        if method == "get_scene_info":
            return {"result": {"object_count": 240, "objects": [{"name": "Villa_Muro_Sur"}]}}
        if method == "execute_code":
            code = params["code"]
            if "broken(" in code:
                return {"error": {"code": -32000, "message": "SyntaxError: '(' was never closed"}}
            return {"result": {"executed": True}}
        return {"result": {}}

    res = baq.run_agent_turn(
        prompt="Crea villa en lote de 300 m2",
        image_path=None,
        lod="LOD_500_ULTRA_DETALLE",
        operation="creation",
        model_fn=fake_model_generate,
        rpc_fn=fake_bridge_rpc,
        max_retries=3,
    )

    assert res["success"] is True
    assert res["attempts"] == 2
    assert res["object_count"] == 240
    assert len(model_calls) == 2
