#!/usr/bin/env python3
"""
Prueba en vivo de Gemini Teacher (API Key o Vertex AI) vs Modelo Bespoke
para generación imagen-a-imagen de código Python bpy con validación en el
Morphs Blender Bridge (http://127.0.0.1:8765/rpc) y guardado de .blend.
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generar_dataset_gold import SYSTEM_PROMPT_GOLD, verify_code_on_bridge


def _encode_image_resized(image_path: Path, max_side: int = 1536) -> Tuple[str, str]:
    with Image.open(image_path) as im:
        rgb = im.convert("RGB")
        w, h = rgb.size
        if max(w, h) > max_side:
            scale = max_side / float(max(w, h))
            rgb = rgb.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        rgb.save(buf, format="JPEG", quality=90)
        return base64.b64encode(buf.getvalue()).decode("ascii"), "image/jpeg"


def call_gemini_vision(
    image_path: Path,
    prompt_text: str,
    model_name: str = "gemini-3.1-pro-preview",
    api_key: Optional[str] = None,
    vertex_project: str = "swift-casing-451920-t7",
) -> str:
    img_b64, mime = _encode_image_resized(image_path)

    payload = {
        "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT_GOLD}]},
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"inlineData": {"mimeType": mime, "data": img_b64}},
                    {"text": prompt_text},
                ],
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 65536,
        },
    }

    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
        headers = {"Content-Type": "application/json"}
    else:
        token = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True).strip()
        url = (
            f"https://us-central1-aiplatform.googleapis.com/v1/projects/{vertex_project}"
            f"/locations/us-central1/publishers/google/models/{model_name}:generateContent"
        )
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        if model_name != "gemini-3.1-pro-preview" and key:
            fallback_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent?key={key}"
            req_fb = urllib.request.Request(
                fallback_url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST"
            )
            with urllib.request.urlopen(req_fb, timeout=180) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        else:
            raise exc
    return data["candidates"][0]["content"]["parts"][0]["text"]


def extract_python_block(response_text: str) -> str:
    if "```python" in response_text:
        return response_text.split("```python", 1)[1].split("```", 1)[0].strip()
    if "```" in response_text:
        return response_text.split("```", 1)[1].split("```", 1)[0].strip()
    return response_text.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Prueba Gemini Vision Teacher sobre una imagen HD y valida en Blender Bridge.")
    parser.add_argument("--image", type=Path, required=True, help="Ruta de la imagen HD a reconstruir.")
    parser.add_argument("--output-blend", type=Path, required=True, help="Ruta donde guardar el .blend resultante.")
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-3.1-pro-preview",
        help="Modelo Gemini Teacher (ej: gemini-3.1-pro-preview, gemini-4-pro, gemini-3.1-flash-preview).",
    )
    parser.add_argument("--min-objects", type=int, default=350, help="Mínimo de objetos 3D exigidos en escena (default: 350).")
    parser.add_argument("--api-key", type=str, default=None, help="GEMINI_API_KEY opcional.")
    parser.add_argument("--bridge-url", type=str, default="http://127.0.0.1:8765/rpc", help="URL del Morphs Blender Bridge.")
    args = parser.parse_args()

    prompt = (
        "[NIVEL_DISENO: LOD_500_ULTRA_DETALLE] [CIERRE: 360_6_CARAS]\n"
        f"Analiza minuciosamente esta imagen arquitectónica y construye una escena de ULTRA-DETALLE con al menos "
        f"{args.min_objects} objetos paramétricos en Blender 5.2 (usando bmesh e instanciación de mallas para baldosas, "
        "lamas, barrotes, carpinterías, mobiliario, follaje y luces LED).\n"
        "REGLAS ESTRICTAS DE COMPATIBILIDAD BLENDER 5.2:\n"
        "1. Antes de limpiar objetos existentes, cambia siempre el viewport a 'SOLID' para evitar crash de GPU.\n"
        "2. Nunca llames a bpy.data.materials.remove() ni bpy.data.meshes.remove().\n"
        "3. En ShaderNodeTexSky usa sky_type = 'MULTIPLE_SCATTERING' (nunca 'NISHITA').\n"
        "4. En Principled BSDF usa 'Base Color', 'Roughness', 'Metallic', 'Alpha', 'Transmission Weight', 'Emission Color' y 'Emission Strength'.\n"
        "5. Al final del script configura scene.camera y pon el viewport 3D en view_perspective = 'CAMERA' y shading.type = 'MATERIAL'.\n"
        "Emite primero el bloque <plan_arquitectonico> JSON con 'cierre_6_caras' y luego el script Python bpy completo "
        "en 360 grados dentro de ```python ... ```."
    )

    resp_text = call_gemini_vision(args.image, prompt, model_name=args.model, api_key=args.api_key)
    code = extract_python_block(resp_text)

    for attempt in range(1, 4):
        ok, count, err = verify_code_on_bridge(code, args.bridge_url, args.output_blend)
        if ok and count >= args.min_objects:
            out_py = args.output_blend.with_suffix(".py")
            out_py.write_text(code, encoding="utf-8")
            out_resp = args.output_blend.with_suffix(".response.txt")
            out_resp.write_text(resp_text, encoding="utf-8")
            print(f"[OK Gemini Teacher ({args.model})] Intento {attempt}: {count} objetos creados -> {args.output_blend}")
            return 0
        reason = err if not ok else f"Densidad insuficiente: solo creó {count} objetos y se exigen >= {args.min_objects}."
        print(f"[Reintento {attempt}] {reason}")
        fix_prompt = (
            f"{prompt}\n\nEl intento anterior no cumplió el estándar en Blender 5.2:\n{reason}\n"
            f"Reescribe el script Python bpy completo superando los {args.min_objects} objetos (desglosando "
            "baldosas individuales, lamas de celosía/persianas, barrotes, marcos de carpintería, tiras LED y "
            "vegetación multi-capa) y devuélvelo dentro de ```python ... ```."
        )
        resp_text = call_gemini_vision(args.image, fix_prompt, model_name=args.model, api_key=args.api_key)
        code = extract_python_block(resp_text)

    print("Falló tras 3 intentos.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
