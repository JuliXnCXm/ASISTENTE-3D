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
  # inferencia aumentada (no toca el entrenamiento):
  python EVALUATION/generar_con_modelo.py --solo_lora --rag_firmas 6 --reparar 2

--rag_firmas K : añade al pedido las K firmas del DSL más relevantes (RAG sobre blender_arch.py)
--sanear       : quita de forma determinista (sin modelo) los argumentos que el DSL no acepta
--reparar N    : hasta N rondas de validación (estática de API + ejecución en Blender) y
                 corrección; el modelo recibe su propio código como 'Código base' (formato
                 de las tareas de edición del dataset) junto al error y las firmas reales.
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
    ("gen_torre_nucleo", "Diseña una torre de 20 pisos de 30x30 metros con núcleo central de hormigón, columnas perimetrales y muro cortina de vidrio."),
    ("gen_torre_girada", "Crea una torre residencial de 25 pisos con planta de 20x20 metros que gire 2 grados en cada piso."),
    ("gen_cocina", "Diseña una cocina de 4x3 metros con mesón en L, una mesa con cuatro sillas y una ventana."),
    ("gen_sala", "Modela una sala de estar de 6x5 metros con un sofá, una mesa de centro, dos sillas y una ventana grande."),
    ("gen_nave_industrial", "Genera una nave industrial de 30x20 metros y 8 metros de altura con columnas de acero cada 6 metros y cubierta plana."),
    ("gen_casa_1p", "Diseña una casa de un piso de 12x9 metros con tres habitaciones, un baño, cocina y sala comedor."),
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


def preparar_multimodal(mm, fuente_profundidad="estimada"):
    """Mismo formato que train_qlora_multimodal.py: RGB + profundidad + texto de cámara.
    fuente_profundidad='estimada' usa Depth Anything + ancla (*_depth_est.npz); 'gt' el EXR."""
    sys.path.insert(0, os.path.join(ROOT, "TRAINING"))
    import train_qlora_multimodal as T
    bloques, cam_txt = [], ""
    rgb = resolver_imagen(mm.get("image"))
    if rgb:
        bloques.append(("Fotografía de referencia (RGB):", Image.open(rgb).convert("RGB")))
    dep = mm.get("metric_depth")
    if dep and fuente_profundidad == "estimada":
        dep = dep.replace("_depth.exr", "_depth_est.npz")
    dep = resolver_imagen(dep)
    if dep and fuente_profundidad == "estimada":
        res = T.cargar_profundidad_estimada(dep)
        if res:
            dimg, lo, hi = res
            bloques.append((f"Mapa de profundidad estimada (claro = cerca; rango aprox. {lo:.1f}–{hi:.1f} m):", dimg))
    elif dep:
        res = T.cargar_profundidad(dep)
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


def texto_rag(prompt, recuperador, k):
    from dsl_api import formatear_firmas
    return "\n\nFunciones del DSL blender_arch relevantes (firmas exactas):\n" + \
        formatear_firmas(recuperador.buscar(prompt, k))


def texto_reparacion(code, errs, prompt, recuperador):
    from dsl_api import FIRMAS, formatear_firmas
    firmas = []
    for e in errs:
        firmas += recuperador.para_error(e)
    firmas = list(dict.fromkeys(firmas))[:6]
    lista = ", ".join(sorted(FIRMAS))
    instr = ("Corrige el código para que se ejecute sin errores en Blender.\nErrores:\n" +
             "\n".join(f"- {e['msg']}" for e in errs[:6]) +
             f"\nFunciones que existen en blender_arch (no hay otras): {lista}.")
    if firmas:
        instr += "\nFirmas exactas útiles:\n" + formatear_firmas(firmas)
    instr += ("\nUsa solo funciones y argumentos que existan; lo que no tenga función propia "
              "constrúyelo con las funciones existentes o con bpy. Mantén el resto del código y lo "
              f"pedido originalmente: \"{prompt.strip()}\"")
    return f"Código base:\n```python\n{code}\n```\nInstrucción: {instr}"


def validar(code, blender, carpeta, nombre):
    """Errores de API (estáticos) o de ejecución en Blender. [] = el código corre."""
    from dsl_api import validar_estatico
    errs = validar_estatico(code)
    if errs or not blender:
        return errs
    from ejecutar_en_blender import evaluar
    py = os.path.join(carpeta, nombre + ".py")
    open(py, "w").write(code)
    r = evaluar(py, blender, timeout=120)
    if r.get("ok"):
        return []
    msg = str(r.get("error"))
    if r.get("linea"):
        msg += f" (en: {r['linea'].split(', in ')[0].split(', ')[-1]})"
    return [dict(tipo="ejecucion", msg=msg)]


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
    ap.add_argument("--fuente_profundidad", choices=["estimada", "gt", "ninguna"], default="estimada")
    ap.add_argument("--max_new_tokens", type=int, default=2048)
    ap.add_argument("--rag_firmas", type=int, default=0, help="K firmas del DSL recuperadas por pedido")
    ap.add_argument("--reparar", type=int, default=0, help="rondas máximas de validación + corrección")
    ap.add_argument("--blender", default="/snap/bin/blender", help="'' = solo validación estática")
    ap.add_argument("--sanear", action="store_true", help="quitar argumentos inexistentes del DSL (sin modelo)")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    sys.path.insert(0, HERE)
    recuperador = None
    if args.rag_firmas or args.reparar:
        from dsl_api import RecuperadorFirmas
        recuperador = RecuperadorFirmas()
    dir_intentos = os.path.join(args.out, "intentos")
    if args.reparar:
        os.makedirs(dir_intentos, exist_ok=True)

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
        bloques, cam_txt = preparar_multimodal(
            {k: v for k, v in caso["mm"].items() if not (k == "metric_depth" and args.fuente_profundidad == "ninguna")},
            args.fuente_profundidad) if caso["mm"] else ([], "")
        pedido = caso["prompt"]
        if recuperador and args.rag_firmas:
            pedido = pedido.replace("<image>\n", "").strip() + texto_rag(caso["prompt"], recuperador, args.rag_firmas)
        imgs = [im for _, im in bloques] or None

        def generar(texto_usuario, var):
            msgs = construir_mensajes(texto_usuario, bloques, cam_txt)
            text = processor.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
            inputs = processor(text=[text], images=imgs, return_tensors="pt").to(model.device)
            with torch.no_grad():
                if var == "base":
                    with model.disable_adapter():
                        out = model.generate(**inputs, max_new_tokens=args.max_new_tokens,
                                             do_sample=False, repetition_penalty=1.05)
                else:
                    out = model.generate(**inputs, max_new_tokens=args.max_new_tokens,
                                         do_sample=False, repetition_penalty=1.05)
            gen = out[0][inputs.input_ids.shape[1]:]
            return limpiar_codigo(processor.decode(gen, skip_special_tokens=True)), len(gen)

        for var in variantes:
            t0 = time.time()
            nombre = f"{caso['id']}__{var}"
            code, ntok = generar(pedido, var)
            tokens, truncado, historial, saneos = ntok, ntok >= args.max_new_tokens, [], []

            def _sanear(c):
                if not (args.sanear and var == "lora"):
                    return c
                from dsl_api import sanear
                c, cambios = sanear(c)
                saneos.extend(cambios)
                return c

            code = _sanear(code)
            if var == "lora":
                for it in range(args.reparar):
                    errs = validar(code, args.blender, dir_intentos, f"{nombre}_i{it}")
                    historial.append([e["msg"] for e in errs])
                    if not errs:
                        break
                    print(f"  [{nombre}] ronda {it + 1}: {errs[0]['msg'][:110]}", flush=True)
                    code, ntok = generar(texto_reparacion(code, errs, caso["prompt"], recuperador), var)
                    code = _sanear(code)
                    tokens += ntok
                    truncado = ntok >= args.max_new_tokens
            dt = time.time() - t0
            with open(os.path.join(args.out, nombre + ".py"), "w") as f:
                f.write(code)
            r = dict(id=caso["id"], tipo=caso["tipo"], variante=var, prompt=caso["prompt"],
                     n_imagenes=len(bloques), tokens=tokens, segundos=round(dt, 1),
                     truncado=truncado, archivo=nombre + ".py",
                     rondas_reparacion=max(0, len(historial) - (0 if historial and historial[-1] else 1))
                     if historial else 0, errores_por_ronda=historial, saneado=saneos)
            resultados.append(r)
            print(f"[{nombre}] {tokens} tokens en {dt:.0f}s rondas={r['rondas_reparacion']}"
                  f"{'  (TRUNCADO)' if r['truncado'] else ''}", flush=True)
        if caso["referencia"]:
            with open(os.path.join(args.out, f"{caso['id']}__referencia.py"), "w") as f:
                f.write(limpiar_codigo(caso["referencia"]))
        json.dump(resultados, open(os.path.join(args.out, "generacion.json"), "w"),
                  ensure_ascii=False, indent=2)
    print("Listo:", args.out)


if __name__ == "__main__":
    main()
