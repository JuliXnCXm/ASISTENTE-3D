#!/usr/bin/env python3
"""
generar_con_modelo.py
Carga Qwen2.5-VL-7B + LoRA (julianG99/qwen2.5-vl-aec-lora) en 4 bits (cabe en 12 GB)
y genera código para una batería de prompts, usando EXACTAMENTE el mismo formato
de mensajes que train_qlora_multimodal.py. Genera también con el modelo base
(adaptador desactivado) para comparar.

Uso:
  python EVALUATION/generar_con_modelo.py --out EVALUATION/resultados_local
  python EVALUATION/generar_con_modelo.py --solo_lora --n_test 10
"""
import argparse, json, os, re, sys, time
import torch
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor, BitsAndBytesConfig
from peft import PeftModel
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SYSTEM = ("Eres un experto en desarrollo arquitectónico CAD procedural-paramétrico.\n"
          "Tu tarea es generar código Python ejecutable en Blender usando el DSL 'blender_arch' y la API 'bpy'.\n"
          "Escribe únicamente código Python autocontenido, sin markdown adicional ni explicaciones.")

# Prompts de generalización (fuera del set de test, escritos a mano)
GENERALIZACION = [
    ("gen_casa_2p", "Diseña una casa de dos pisos de 8x10 metros con tejado a dos aguas, una puerta principal y ventanas en la fachada frontal."),
    ("gen_oficinas_8p", "Genera un edificio de oficinas de 8 pisos de 20x15 metros con columnas estructurales de hormigón y ventanas en la fachada."),
    ("gen_rascacielos_30p", "Diseña un rascacielos de 30 pisos con planta cuadrada de 24x24 metros, estructura de columnas y fachada de vidrio."),
    ("gen_habitacion", "Crea un dormitorio de 4x3.5 metros con una cama doble, un armario y una ventana."),
    ("gen_escalera", "Modela una escalera recta de 14 peldaños con barandas a ambos lados que conecte dos pisos de 2.8 m."),
]


def leer_jsonl_tolerante(path):
    s = open(path, encoding="utf-8").read()
    dec, i, rows = json.JSONDecoder(), 0, []
    while i < len(s):
        while i < len(s) and s[i] in " \n\t\r,[]":
            i += 1
        if i >= len(s):
            break
        o, i = dec.raw_decode(s, i)
        rows.append(o)
    return rows


def resolver_imagen(p):
    if not p:
        return None
    for cand in (p, os.path.join(ROOT, p), os.path.join(ROOT, "DATASET", p)):
        if os.path.exists(cand):
            return cand
    return None


def preparar_multimodal(mm):
    """Mismo formato que train_qlora_multimodal.py: RGB + profundidad métrica + texto de cámara."""
    sys.path.insert(0, os.path.join(ROOT, "TRAINING"))
    import train_qlora_multimodal as T
    bloques, cam_txt = [], ""
    rgb = resolver_imagen(mm.get("image"))
    if rgb:
        bloques.append(("Fotografía de referencia (RGB):", Image.open(rgb).convert("RGB")))
    exr = resolver_imagen(mm.get("metric_depth"))
    if exr:
        res = T.cargar_profundidad(exr)
        if res:
            dimg, lo, hi = res
            bloques.append((f"Mapa de profundidad métrica (claro = cerca; rango {lo:.1f}–{hi:.1f} m):", dimg))
    cam = resolver_imagen(mm.get("camera"))
    if cam:
        cam_txt = T.texto_camara(cam)
    return bloques, cam_txt


def construir_mensajes(texto, bloques=(), cam_txt=""):
    content = []
    for intro, _ in bloques:
        content.append({"type": "text", "text": intro})
        content.append({"type": "image"})
    texto = texto.replace("<image>\n", "").strip()
    content.append({"type": "text", "text": f"Instrucción del usuario: {texto}{cam_txt}"})
    return [{"role": "system", "content": [{"type": "text", "text": SYSTEM}]},
            {"role": "user", "content": content}]


def limpiar_codigo(txt):
    m = re.search(r"```(?:python)?\s*(.*?)```", txt, re.DOTALL)
    return (m.group(1) if m else txt).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="Qwen/Qwen2.5-VL-7B-Instruct")
    ap.add_argument("--lora", default="julianG99/qwen2.5-vl-aec-lora")
    ap.add_argument("--out", default=os.path.join(HERE, "resultados_local"))
    ap.add_argument("--n_test", type=int, default=6, help="prompts 'creation' del test split")
    ap.add_argument("--con_imagen", action="store_true", help="pasar la imagen RGB del test split")
    ap.add_argument("--solo_lora", action="store_true")
    ap.add_argument("--max_new_tokens", type=int, default=2048)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    casos = []
    test = leer_jsonl_tolerante(os.path.join(ROOT, "TRAINING/data/test_multimodal.jsonl"))
    for r in [r for r in test if r["task_type"] == "creation"][:args.n_test]:
        user = next(m["content"] for m in r["messages"] if m["role"] == "user")
        ref = next(m["content"] for m in r["messages"] if m["role"] == "assistant")
        mm = r.get("multimodal", {}) if args.con_imagen else {}
        casos.append(dict(id=f"test_{r['id']}", tipo="test", prompt=user.replace("<image>\n", ""),
                          mm=mm, referencia=ref))
    for cid, p in GENERALIZACION:
        casos.append(dict(id=cid, tipo="generalizacion", prompt=p, mm={}, referencia=None))

    print(f"Cargando {args.base} en 4 bits + LoRA {args.lora} ...")
    bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                             bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=torch.bfloat16)
    processor = AutoProcessor.from_pretrained(args.base, min_pixels=256 * 28 * 28, max_pixels=512 * 28 * 28)
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        args.base, quantization_config=bnb, device_map="cuda:0", torch_dtype=torch.bfloat16)
    model = PeftModel.from_pretrained(model, args.lora)
    model.eval()
    print(f"VRAM usada: {torch.cuda.memory_allocated() / 1e9:.1f} GB")

    variantes = ["lora"] if args.solo_lora else ["lora", "base"]
    resultados = []
    for caso in casos:
        bloques, cam_txt = preparar_multimodal(caso["mm"]) if caso["mm"] else ([], "")
        msgs = construir_mensajes(caso["prompt"], bloques, cam_txt)
        text = processor.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
        imgs = [im for _, im in bloques] or None
        inputs = processor(text=[text], images=imgs, return_tensors="pt").to(model.device)
        for var in variantes:
            t0 = time.time()
            with torch.no_grad():
                if var == "base":
                    with model.disable_adapter():
                        out = model.generate(**inputs, max_new_tokens=args.max_new_tokens,
                                             do_sample=False, repetition_penalty=1.05)
                else:
                    out = model.generate(**inputs, max_new_tokens=args.max_new_tokens,
                                         do_sample=False, repetition_penalty=1.05)
            gen = out[0][inputs.input_ids.shape[1]:]
            txt = processor.decode(gen, skip_special_tokens=True)
            code = limpiar_codigo(txt)
            dt = time.time() - t0
            nombre = f"{caso['id']}__{var}"
            with open(os.path.join(args.out, nombre + ".py"), "w") as f:
                f.write(code)
            r = dict(id=caso["id"], tipo=caso["tipo"], variante=var, prompt=caso["prompt"],
                     n_imagenes=len(bloques), tokens=len(gen), segundos=round(dt, 1),
                     truncado=len(gen) >= args.max_new_tokens, archivo=nombre + ".py")
            resultados.append(r)
            print(f"[{nombre}] {len(gen)} tokens en {dt:.0f}s{'  (TRUNCADO)' if r['truncado'] else ''}", flush=True)
        if caso["referencia"]:
            with open(os.path.join(args.out, f"{caso['id']}__referencia.py"), "w") as f:
                f.write(limpiar_codigo(caso["referencia"]))
        json.dump(resultados, open(os.path.join(args.out, "generacion.json"), "w"),
                  ensure_ascii=False, indent=2)
    print("Listo:", args.out)


if __name__ == "__main__":
    main()
