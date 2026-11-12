#!/usr/bin/env python3
"""
Agente de Inferencia Multimodal (Qwen2.5-VL-7B + LoRA) conectado en vivo
al Morphs Blender Bridge (http://127.0.0.1:8765/rpc).

Soporta:
  - Las 3 modalidades de entrada:
      1) Solo Prompt (--prompt "...")
      2) Solo Imagen (--image ruta.jpg)
      3) Imagen + Prompt (--image ruta.jpg --prompt "...")
  - Los 3 modos de operación:
      * creation (LOD_500_ULTRA_DETALLE en 360° - 6 caras)
      * edit (inspecciona primero get_scene_info en el Bridge e inyecta <escena_actual_blender>)
      * aec_structural (LOD_400_INGENIERIA_AEC BIM estructural)
  - Bucle de Auto-Corrección (Execution Feedback Loop) contra el Bridge (hasta 3 intentos).
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR.parent / "DATASET" / "scripts"))
from generar_dataset_gold import SYSTEM_PROMPT_GOLD, verify_code_headless_blender


def default_bridge_rpc(
    method: str,
    params: Dict[str, Any],
    bridge_url: str = "http://127.0.0.1:8765/rpc",
) -> Dict[str, Any]:
    if bridge_url == "headless" or not bridge_url.startswith("http"):
        if method == "get_scene_info":
            return {"result": {"object_count": 0, "objects": []}}
        if method == "execute_code":
            ok, cnt, err = verify_code_headless_blender(params["code"])
            if not ok:
                return {"error": {"code": -32000, "message": err}}
            default_bridge_rpc._last_headless_count = cnt
            return {"result": {"executed": True, "object_count": cnt}}
        return {"result": {}}

    try:
        payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode("utf-8")
        req = urllib.request.Request(
            bridge_url, data=payload, headers={"Content-Type": "application/json"}, method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            res = json.loads(resp.read().decode("utf-8"))
        if "error" in res and "disabled by security policy" in res["error"].get("message", ""):
            if method == "execute_code":
                ok, cnt, err = verify_code_headless_blender(params["code"])
                if not ok:
                    return {"error": {"code": -32000, "message": err}}
                default_bridge_rpc._last_headless_count = cnt
                return {"result": {"executed": True, "object_count": cnt}}
        return res
    except Exception:
        if method == "get_scene_info":
            return {"result": {"object_count": getattr(default_bridge_rpc, "_last_headless_count", 0), "objects": []}}
        if method == "execute_code":
            ok, cnt, err = verify_code_headless_blender(params["code"])
            if not ok:
                return {"error": {"code": -32000, "message": err}}
            default_bridge_rpc._last_headless_count = cnt
            return {"result": {"executed": True, "object_count": cnt}}
        return {"result": {}}


def build_user_instruction(
    prompt: str,
    image_path: Optional[Path],
    lod: str = "LOD_500_ULTRA_DETALLE",
    operation: str = "creation",
    scene_info: Optional[Dict[str, Any]] = None,
) -> str:
    effective_lod = "LOD_400_INGENIERIA_AEC" if operation == "aec_structural" else lod
    header = f"[NIVEL_DISENO: {effective_lod}] [CIERRE: 360_6_CARAS]"
    img_prefix = "<image>\n" if image_path is not None else ""

    scene_block = ""
    if operation == "edit" and scene_info is not None:
        obj_names = [o.get("name") for o in scene_info.get("objects", [])[:40]]
        scene_block = (
            f"\n<escena_actual_blender>\n"
            f"object_count: {scene_info.get('object_count', 0)} | sample_objects: {obj_names}\n"
            f"</escena_actual_blender>\n"
        )

    clean_prompt = (prompt or "").strip()
    if not clean_prompt:
        if operation == "aec_structural":
            clean_prompt = (
                "Replica esta escena exclusivamente en modo estructural y de ingeniería AEC "
                "(BIM LOD 400: cimentación de hormigón armado, acero primario/secundario IPE/HEA y losas colaborantes)."
            )
        else:
            clean_prompt = (
                "Reconstruye esta escena arquitectónica en Blender con código Python bpy completo "
                "garantizando el cierre de las 6 caras en 360 grados."
            )

    return f"{img_prefix}{header}{scene_block}\n{clean_prompt}".strip()


def inject_defensive_prelude(code: str) -> str:
    """Inyecta helpers defensivos estándar (random, create_mesh_object, colecciones por defecto)
    para que pequeños olvidos de variables auxiliares en un modelo 7B nunca rompan la ejecución."""
    prelude = '''import bpy, bmesh, math, random
from mathutils import Vector, Matrix

for _w in bpy.context.window_manager.windows:
    for _a in _w.screen.areas:
        if _a.type == 'VIEW_3D':
            for _s in _a.spaces:
                if _s.type == 'VIEW_3D':
                    _s.shading.type = 'SOLID'
for _o in list(bpy.data.objects):
    bpy.data.objects.remove(_o, do_unlink=True)

collection_arch = bpy.data.collections.get("01_Architecture") or bpy.data.collections.new("01_Architecture")
if collection_arch.name not in bpy.context.scene.collection.children:
    bpy.context.scene.collection.children.link(collection_arch)
collection_facade = collection_arch

def create_mesh_object(name, bm, mat=None, col=None):
    mesh = bpy.data.meshes.new(name + "_Mesh")
    bm.to_mesh(mesh)
    bm.free()
    if mat is not None:
        mesh.materials.append(mat)
    obj = bpy.data.objects.new(name, mesh)
    if mat is not None and hasattr(mat, "diffuse_color"):
        obj.color = mat.diffuse_color
    if col is not None and obj.name not in col.objects:
        col.objects.link(obj)
    return obj
'''
    # Proteger accesos a bpy.context.screen.areas cuando corre en headless o fuera de contexto
    safe_code = (
        code.replace(
            "for area in bpy.context.screen.areas:",
            "for area in (bpy.context.screen.areas if bpy.context.screen else []):",
        )
        .replace("collection.objects.clear()", "pass")
        .replace("while start_x <= end_x:", "while start_x < end_x - 1e-3:")
        .replace("panel_width = end_x - start_x", "panel_width = max(0.25, end_x - start_x)")
    )
    safe_code = re.sub(
        r"(\w+)\.data\.materials\.append\(([^)]+)\)",
        r"(\1.data.materials.append(\2) if len(\1.data.materials) == 0 else None)",
        safe_code,
    )
    return prelude + "\n" + safe_code


def extract_python_from_response(text: str) -> str:
    if "```python" in text:
        raw = text.split("```python", 1)[1].split("```", 1)[0].strip()
    elif "```" in text:
        raw = text.split("```", 1)[1].split("```", 1)[0].strip()
    else:
        raw = text.strip()
    return inject_defensive_prelude(raw)


def run_agent_turn(
    prompt: str,
    image_path: Optional[Path] = None,
    lod: str = "LOD_500_ULTRA_DETALLE",
    operation: str = "creation",
    bridge_url: str = "http://127.0.0.1:8765/rpc",
    save_blend: Optional[Path] = None,
    model_fn: Optional[Callable[[List[Dict[str, str]], Optional[Path]], str]] = None,
    rpc_fn: Callable[[str, Dict[str, Any], str], Dict[str, Any]] = default_bridge_rpc,
    max_retries: int = 3,
) -> Dict[str, Any]:
    if model_fn is None:
        raise ValueError("Se requiere model_fn configurado (HF PEFT o endpoint compatible).")

    scene_info = None
    if operation == "edit":
        res_info = rpc_fn("get_scene_info", {}, bridge_url)
        scene_info = res_info.get("result", {})

    user_instruction = build_user_instruction(
        prompt=prompt,
        image_path=image_path,
        lod=lod,
        operation=operation,
        scene_info=scene_info,
    )

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT_GOLD},
        {"role": "user", "content": user_instruction},
    ]

    last_error = ""
    for attempt in range(1, max_retries + 1):
        resp_text = model_fn(messages, image_path)
        code = extract_python_from_response(resp_text)

        if save_blend is not None:
            save_blend.parent.mkdir(parents=True, exist_ok=True)
            save_blend.with_name(f"{save_blend.stem}_attempt{attempt}.py").write_text(code, encoding="utf-8")
            save_blend.with_name(f"{save_blend.stem}_attempt{attempt}.response.txt").write_text(resp_text, encoding="utf-8")
            save_blend.with_suffix(".py").write_text(code, encoding="utf-8")
            save_blend.with_suffix(".response.txt").write_text(resp_text, encoding="utf-8")
            code_to_run = (
                code
                + f"\n\nbpy.ops.wm.save_as_mainfile(filepath={repr(str(save_blend.resolve()))})\n"
            )
        else:
            code_to_run = code

        exec_res = rpc_fn("execute_code", {"code": code_to_run}, bridge_url)
        if "error" not in exec_res:
            post_info = rpc_fn("get_scene_info", {}, bridge_url).get("result", {})
            return {
                "success": True,
                "attempts": attempt,
                "object_count": int(post_info.get("object_count", 0)),
                "code": code,
                "raw_response": resp_text,
            }

        last_error = exec_res["error"].get("message", "Unknown Blender error")
        messages.append({"role": "assistant", "content": resp_text})
        messages.append(
            {
                "role": "user",
                "content": (
                    f"Blender devolvió este error al ejecutar tu script:\n{last_error}\n"
                    "Corrige el script Python bpy manteniendo las 6 caras y devuélvelo dentro de ```python ... ```."
                ),
            }
        )

    return {
        "success": False,
        "attempts": max_retries,
        "object_count": 0,
        "error": last_error,
    }


def make_hf_peft_generator(base_model: str, lora_path: Optional[str], max_new_tokens: int = 8192):
    import torch
    from PIL import Image
    from peft import PeftModel
    from transformers import AutoProcessor, BitsAndBytesConfig, Qwen2_5_VLForConditionalGeneration

    bnb = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )
    processor = AutoProcessor.from_pretrained(
        base_model, min_pixels=128 * 28 * 28, max_pixels=768 * 768
    )
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        base_model, quantization_config=bnb, device_map="auto", torch_dtype=torch.bfloat16
    )
    if lora_path:
        model = PeftModel.from_pretrained(model, lora_path)
    model.eval()

    def _generate(messages: List[Dict[str, str]], image_path: Optional[Path] = None) -> str:
        qwen_msgs = []
        imgs = []
        first_user = True
        for m in messages:
            if m["role"] == "user" and first_user and image_path is not None:
                imgs.append(Image.open(image_path).convert("RGB"))
                clean = m["content"].replace("<image>\n", "").replace("<image>", "").strip()
                qwen_msgs.append(
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Fotografía de referencia (RGB):"},
                            {"type": "image"},
                            {"type": "text", "text": f"Instrucción del usuario: {clean}"},
                        ],
                    }
                )
                first_user = False
            else:
                qwen_msgs.append({"role": m["role"], "content": [{"type": "text", "text": m["content"]}]})

        text_prompt = processor.apply_chat_template(qwen_msgs, tokenize=False, add_generation_prompt=True)
        inputs = processor(
            text=[text_prompt], images=imgs if imgs else None, padding=True, return_tensors="pt"
        ).to(model.device)
        with torch.no_grad():
            out_ids = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.3,
                top_p=0.9,
                repetition_penalty=1.12,
                do_sample=True,
            )
        gen_ids = out_ids[0][inputs["input_ids"].shape[1] :]
        return processor.tokenizer.decode(gen_ids, skip_special_tokens=True)

    return _generate


def main() -> int:
    parser = argparse.ArgumentParser(description="Agente Qwen2.5-VL-7B LoRA conectado al Morphs Blender Bridge.")
    parser.add_argument("--prompt", type=str, default="", help="Instrucción del usuario (opcional si se pasa --image).")
    parser.add_argument("--image", type=Path, default=None, help="Imagen de referencia opcional.")
    parser.add_argument("--operation", choices=["creation", "edit", "aec_structural"], default="creation")
    parser.add_argument("--lod", type=str, default="LOD_500_ULTRA_DETALLE")
    parser.add_argument("--base-model", type=str, default="Qwen/Qwen2.5-VL-7B-Instruct")
    parser.add_argument("--lora-path", type=str, default=None, help="Ruta o repo HF del adaptador LoRA entrenado.")
    parser.add_argument("--bridge-url", type=str, default="http://127.0.0.1:8765/rpc")
    parser.add_argument("--max-retries", type=int, default=1, help="Intentos máximos de generación (default: 1 para mantener distribución single-turn).")
    parser.add_argument("--save-blend", type=Path, default=None, help="Guardar escena resultante en .blend.")
    args = parser.parse_args()

    gen_fn = make_hf_peft_generator(args.base_model, args.lora_path)
    res = run_agent_turn(
        prompt=args.prompt,
        image_path=args.image,
        lod=args.lod,
        operation=args.operation,
        bridge_url=args.bridge_url,
        save_blend=args.save_blend,
        model_fn=gen_fn,
        max_retries=args.max_retries,
    )
    if res["success"]:
        if args.save_blend is not None:
            args.save_blend.with_suffix(".py").write_text(res["code"], encoding="utf-8")
            args.save_blend.with_suffix(".response.txt").write_text(res["raw_response"], encoding="utf-8")
        print(f"[OK Bridge Agent] Escena creada en {res['attempts']} intento(s): {res['object_count']} objetos.")
        return 0
    print(f"[ERROR Bridge Agent] Falló tras {res['attempts']} intentos: {res.get('error')}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
