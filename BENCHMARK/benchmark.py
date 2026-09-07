# benchmark.py
import os, json, re, argparse, subprocess, textwrap, sys
from pathlib import Path
import requests, py_compile

ROOT_DIR = Path(__file__).resolve().parent.parent

SYSTEM_PROMPT = textwrap.dedent("""
Eres un asistente que GENERA SOLO CÓDIGO PYTHON para Blender.

REQUISITOS:
- Devuelve ÚNICAMENTE un bloque de código dentro de triple backticks: ```python ... ```
- Usa bpy y funciona en headless (-b), sin operadores que requieran UI.
- Limpia la escena: bpy.ops.wm.read_factory_settings(use_empty=True)
- Crea la geometría solicitada en metros.
- Si deseas guardar .blend, usa la variable de entorno BLEND_OUT si existe.
- No uses add-ons externos, ni internet, ni UI modal.
""").strip()

CODE_BLOCK_RE = re.compile(r"```(?:python)?\s*([\s\S]*?)```", re.IGNORECASE)
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
BLENDER_BIN = os.environ.get("BLENDER_BIN", "blender")
TIMEOUT = int(os.environ.get("BLENDER_TIMEOUT", "900"))


def _normalize_ollama_base(url: str | None) -> str:
    base = (url or "http://localhost:11434").strip().rstrip("/")
    if base.endswith("/api"):
        base = base[:-4]  # quita sufijo /api
    return base

def load_prompts(p: Path):
    if not p.exists():
        raise SystemExit(f"No existe {p.name} en {p}")
    return json.loads(p.read_text(encoding="utf-8"))

def call_ollama(model: str, user_prompt: str, base_url: str = None, system_prompt: str = None, debug: bool = False) -> str:
    base = _normalize_ollama_base(base_url or OLLAMA_HOST)
    system_prompt = system_prompt or SYSTEM_PROMPT
    url = f"{base}/api/chat"

    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "options": {"temperature": 0.2, "num_ctx": 8192}
    }

    sess = requests.Session()
    sess.trust_env = False  # ignora HTTP(S)_PROXY del sistema (localhost)

    if debug:
        print(f"POST {url}  model={model}")

    r = sess.post(url, json=payload, timeout=600)
    r.raise_for_status()
    data = r.json()
    return (data.get("message") or {}).get("content", "")


def extract_code(text: str) -> str:
    blocks = CODE_BLOCK_RE.findall(text)
    if blocks:
        return max(blocks, key=len).strip()
    return text.strip()

def ensure_dir(p: Path): p.mkdir(parents=True, exist_ok=True)

def py_compile_file(pyfile: Path):
    try:
        py_compile.compile(str(pyfile), doraise=True)
        return True, "OK"
    except py_compile.PyCompileError as e:
        return False, str(e)

def run_blender_runner(blender_bin: str, runner: Path, gt_script: Path, pred_script: Path, arch_dir: str, report: Path):
    cmd = [blender_bin, "-b", "-P", str(runner), "--",
           "--gt-script", str(gt_script),
           "--pred-script", str(pred_script),
           "--arch-dir", str(arch_dir),
           "--report", str(report)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
    return proc.returncode, proc.stdout, proc.stderr

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", required=True, help="Modelos Ollama separados por coma (ej: llama3:8b-instruct,mistral:7b-instruct,gemma2:9b-instruct)")
    ap.add_argument("--prompts", default=str(ROOT_DIR / "BENCHMARK" / "prompts.json"))
    ap.add_argument("--outdir", default=str(ROOT_DIR / "BENCHMARK" / "outputs_benchmark"))
    ap.add_argument("--runner", default=str(ROOT_DIR / "EVALUATION" / "evaluate_geometry.py"))
    ap.add_argument("--ollama-host", default=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
                help="Base URL de Ollama sin /api (ej: http://localhost:11434)")
    ap.add_argument("--use_arch_dir", default=str(ROOT_DIR / "DSL" / "blender"), help="Opcional: carpeta con blender_arch.py; se añade a PYTHONPATH en Blender.")
    args = ap.parse_args()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    prompts = load_prompts(Path(args.prompts))
    outdir = Path(args.outdir); ensure_dir(outdir)
    runner = Path(args.runner)
    if not runner.exists(): raise SystemExit(f"No se encontró {runner}")

    summary = []
    for model in models:
        for item in prompts:
            pid = str(item["id"])
            titulo = item.get("titulo","")
            prompt = item["prompt"]
            case_dir = outdir / model.replace(":", "_") / pid
            ensure_dir(case_dir)

            # 1) Query modelo
            try:
                raw = call_ollama(model, prompt, base_url=args.ollama_host, system_prompt=SYSTEM_PROMPT, debug=False)
            except Exception as e:
                (case_dir/"error_ollama.txt").write_text(str(e), encoding="utf-8")
                summary.append({"model":model,"id":pid,"titulo":titulo,"ollama_ok":False,"compile_ok":False,"rc":None})
                continue

            (case_dir/"llm_raw.txt").write_text(raw, encoding="utf-8")
            code = extract_code(raw)
            script = case_dir / f"{pid}_{model.replace(':','_')}.py"
            script.write_text(code, encoding="utf-8")

            # 2) Compilación Python
            comp_ok, comp_msg = py_compile_file(script)
            (case_dir/"compile.log").write_text(comp_msg, encoding="utf-8")
            if not comp_ok:
                summary.append({"model":model,"id":pid,"titulo":titulo,"ollama_ok":True,"compile_ok":False,"rc":None})
                continue

            # 3) Ejecutar Blender runner
            out_blend = case_dir / f"{pid}.blend"
            report = case_dir / "report.json"

            env_arch_dir = args.use_arch_dir.strip()
            if not env_arch_dir:
                env_arch_dir = "../DSL/blender"

            # Create dummy GT script for testing if real not available
            gt_script = case_dir / "gt_script.py"
            if "python_code" in item:
                gt_script.write_text(item["python_code"], encoding="utf-8")
            else:
                gt_script.write_text("import blender_arch\n", encoding="utf-8")

            rc, out, err = run_blender_runner(BLENDER_BIN, runner, gt_script, script, env_arch_dir, report)
            (case_dir/"blender_stdout.log").write_text(out, encoding="utf-8")
            (case_dir/"blender_stderr.log").write_text(err, encoding="utf-8")

            # 4) Leer reporte
            rep = {}
            if report.exists():
                rep = json.loads(report.read_text(encoding="utf-8"))

            summary.append({
                "model": model, "id": pid, "titulo": titulo,
                "ollama_ok": True, "compile_ok": True, "rc": rc,
                "mesh_objects": rep.get("pred_vertices_count",0) > 0, # Simplify to bool for now
                "chamfer_distance": rep.get("chamfer_distance", None),
                "execution_error": rep.get("execution_error", "")
            })

    (outdir/"results_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    # CSV rápido
    cols = ["model","id","titulo","ollama_ok","compile_ok","rc","chamfer_distance","execution_error"]
    lines = [",".join(cols)]
    for r in summary:
        row = [str(r.get(k,"")) for k in cols]
        lines.append(",".join(x.replace("\n"," ").replace(",",";") for x in row))
    (outdir/"results_summary.csv").write_text("\n".join(lines), encoding="utf-8")
    print(f"Listo. Resultados en {outdir}")

if __name__ == "__main__":
    main()
