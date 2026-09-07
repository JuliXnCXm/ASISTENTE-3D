#!/usr/bin/env python3
import os, sys, json, time, re, argparse, subprocess, textwrap, shutil, pathlib
import py_compile
import requests
from datetime import datetime

# -------------------- Config por defecto --------------------
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

DEFAULT_MODELS = [
    "gemma3:12b",
    "mistral-small:22b",
    "gpt-oss:20b",      # Añadida la coma faltante que causaba problemas
    "llama3.1:8b"       # Llama
]

SYSTEM_INSTRUCTIONS = """Eres un asistente que SOLO devuelve código Python para Blender.
Requisitos OBLIGATORIOS:
- Escribe SOLO código Python (sin comentarios ni markdown).
- Debe funcionar dentro de Blender (bpy) o en headless con blender -b.
- IMPORTANTE: Usar la librería 'blender_arch' expuesta como 'import blender_arch as A' o recibir A en globals.
- No uses paquetes externos. No uses UI modal.
- Limpia la escena si es necesario (bpy.ops.wm.read_factory_settings(use_empty=True)).
- El resultado debe crear geometría según el pedido, pero NO guardes archivos.
"""

USER_WRAPPER = """\
Responde SOLO con código Python. No uses ``` ni markdown.
Si usas import, haz: import blender_arch as A; import bpy
Crea la geometría solicitada. No imprimas explicaciones.
"""

# -------------------- Utilidades --------------------
def sanitize_filename(s):
    s = re.sub(r'[^a-zA-Z0-9_.-]+', '_', s)
    return s.strip('_')[:80] or "untitled"

def extract_python(text):
    """
    Devuelve el primer bloque de código Python si viene en ```python ...```, o todo el texto sin fences.
    """
    fence = re.findall(r"```(?:python)?\s*([\s\S]*?)```", text, flags=re.IGNORECASE)
    if fence:
        return fence[0].strip()
    # strip common junk
    return text.strip()

def save_text(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def run_py_compile(code_path):
    try:
        py_compile.compile(code_path, doraise=True)
        return True, ""
    except py_compile.PyCompileError as e:
        return False, str(e)

def call_ollama(model, prompt, system=SYSTEM_INSTRUCTIONS):
    url = f"{OLLAMA_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system,
        "stream": False,
        "options": {"temperature": 0.2}
    }
    r = requests.post(url, json=payload, timeout=600)
    r.raise_for_status()
    data = r.json()
    return data.get("response", "")

def query_model(model, prompt):

    text = call_ollama(model, USER_WRAPPER + "\n" + prompt)
    return text

def write_blender_wrapper(wrapper_path):
    code = r'''
import os, sys, json, argparse, traceback
import bpy, bmesh

def validar_malla_obj(obj):
    me = obj.data
    bm = bmesh.new(); bm.from_mesh(me)
    non_manifold = sum(1 for e in bm.edges if not e.is_manifold)
    zero_area = sum(1 for f in bm.faces if f.calc_area() <= 1e-12)
    bm.free()
    changed = me.validate(verbose=False)
    me.update()
    return {
        "name": obj.name,
        "non_manifold_edges": non_manifold,
        "zero_area_faces": zero_area,
        "mesh_validate_fixed": bool(changed),
        "verts": len(me.vertices),
        "edges": len(me.edges),
        "faces": len(me.polygons)
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--code", required=True)
    ap.add_argument("--arch_dir", required=True)
    ap.add_argument("--out_blend", required=False)
    ap.add_argument("--report", required=True)
    args, extra = ap.parse_known_args(sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else [])

    # preparar entorno
    if args.arch_dir not in sys.path:
        sys.path.insert(0, args.arch_dir)
    import blender_arch as A

    # escena limpia
    bpy.ops.wm.read_factory_settings(use_empty=True)

    ok = True; err = ""
    try:
        # ejecutar el código generado por el LLM
        _g = {"bpy": bpy, "A": A}
        with open(args.code, "r", encoding="utf-8") as f:
            src = f.read()
        exec(compile(src, args.code, "exec"), _g, _g)
    except Exception as e:
        ok = False
        err = traceback.format_exc()

    # recolectar métricas de mallas
    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    report = {
        "exec_ok": ok,
        "exec_error": err,
        "mesh_count": len(meshes),
        "meshes": []
    }
    for o in meshes:
        try:
            report["meshes"].append(validar_malla_obj(o))
        except Exception:
            report["meshes"].append({"name": o.name, "validation_error": True})

    # guardar blend si se pide
    if args.out_blend:
        try:
            bpy.ops.wm.save_as_mainfile(filepath=args.out_blend)
            report["blend_saved"] = args.out_blend
        except Exception as e:
            report["blend_save_error"] = str(e)

    # volcar json
    os.makedirs(os.path.dirname(args.report), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    main()
'''
    save_text(wrapper_path, code)

def run_blender_validation(blender_bin, arch_dir, gt_script_path, pred_script_path, eval_script, report_path, timeout=900):
    cmd = [
        blender_bin, "-b", "-P", eval_script, "--",
        "--gt-script", gt_script_path,
        "--pred-script", pred_script_path,
        "--arch-dir", arch_dir,
        "--report", report_path
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, text=True)
        return res.returncode, res.stdout, res.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT"

# -------------------- Main --------------------
def main():
    parser = argparse.ArgumentParser(description="Benchmark LLMs -> Blender Python via Ollama/OpenAI")
    parser.add_argument("--prompts", required=True, help="Ruta a prompts.json")
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS, help="Lista de modelos (ollama tags o gpt-*)")
    parser.add_argument("--outdir", default="out_runs", help="Directorio de resultados")
    parser.add_argument("--blender", help="Ruta a binario de Blender para validación en headless")
    parser.add_argument("--arch_dir", default="../DSL/blender", help="Carpeta con blender_arch.py")
    parser.add_argument("--saveblend", action="store_true", help="Guardar .blend por caso")
    parser.add_argument("--eval_script", default="../EVALUATION/evaluate_geometry.py", help="Ruta al script de evaluación de Chamfer Distance")
    args = parser.parse_args()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(args.outdir, ts)
    os.makedirs(run_dir, exist_ok=True)

    with open(args.prompts, "r", encoding="utf-8") as f:
        prompts = json.load(f)

    summary = []
    for model in args.models:
        model_dir = os.path.join(run_dir, sanitize_filename(model))
        os.makedirs(model_dir, exist_ok=True)
        for item in prompts:
            pid = item["id"]; title = item["title"]; prompt = item["prompt"]
            case_dir = os.path.join(model_dir, f"{pid:02d}_{sanitize_filename(title)}")
            os.makedirs(case_dir, exist_ok=True)

            # ---- Query
            try:
                resp = query_model(model, prompt)
            except Exception as e:
                save_text(os.path.join(case_dir, "error_query.txt"), str(e))
                summary.append({"model": model, "id": pid, "title": title, "query_error": str(e)})
                continue

            raw_path = os.path.join(case_dir, "raw_response.txt")
            save_text(raw_path, resp)

            code = extract_python(resp)
            code_path = os.path.join(case_dir, "code.py")
            save_text(code_path, code)

            # ---- Compile check
            ok_compile, err_compile = run_py_compile(code_path)
            save_text(os.path.join(case_dir, "compile.txt"), "OK" if ok_compile else ("ERROR\n"+err_compile))

            result = {
                "model": model,
                "id": pid,
                "title": title,
                "compile_ok": ok_compile
            }

            # ---- Blender validation (opcional)
            if args.blender:
                out_blend = os.path.join(case_dir, "scene.blend") if args.saveblend else ""
                report_path = os.path.join(case_dir, "report.json")
                rc, out, err = run_blender_validation(
                    blender_bin=args.blender,
                    arch_dir=os.path.abspath(args.arch_dir),
                    code_path=code_path,
                    out_blend=out_blend,
                    report_path=report_path
                )
                save_text(os.path.join(case_dir, "blender_stdout.txt"), out)
                save_text(os.path.join(case_dir, "blender_stderr.txt"), err)
                result.update({"blender_rc": rc, "report": report_path if os.path.exists(report_path) else None})
            summary.append(result)

    # ---- Guardar resumen
    save_text(os.path.join(run_dir, "summary.json"), json.dumps(summary, indent=2))
    print(f"Listo. Resultados en: {run_dir}")

if __name__ == "__main__":
    main()
