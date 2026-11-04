# benchmark.py
import os, json, re, argparse, subprocess, textwrap, sys
from pathlib import Path
import requests, py_compile

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from RAG.retrieval import Retriever
except ImportError:
    Retriever = None

SYSTEM_PROMPT = textwrap.dedent("""
Eres un asistente experto en arquitectura y desarrollo CAD procedural-paramétrico.
Genera SOLO CÓDIGO PYTHON ejecutable en Blender usando la librería `blender_arch` importada como `A`, o la API `bpy`.

REQUISITOS:
- Devuelve ÚNICAMENTE el bloque de código Python, dentro de triple backticks: ```python ... ```
- La primera línea debe ser siempre: import blender_arch as A
- Inicia limpiando la escena: A.limpiar_escena()
- No uses paquetes externos, ni internet, ni UI modal.
""").strip()

REPAIR_PROMPT = textwrap.dedent("""
El código Python que generaste falló al ejecutarse. 
Este fue el error exacto:

{error}

Por favor, analiza el error y devuelve el script de Python completo, corregido y funcional.
Recuerda devolver SOLO el bloque de código Python.
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

    r = sess.post(url, json=payload, timeout=1800) # Timeout subido a 30 minutos (1800s) para cambio de modelos
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
    ap.add_argument("--models", required=True, help="Modelos Ollama/vLLM separados por coma")
    ap.add_argument("--prompts", default=str(ROOT_DIR / "BENCHMARK" / "prompts.json"))
    ap.add_argument("--outdir", default=str(ROOT_DIR / "BENCHMARK" / "outputs_benchmark"))
    ap.add_argument("--runner", default=str(ROOT_DIR / "EVALUATION" / "evaluate_geometry.py"))
    ap.add_argument("--ollama-host", default=os.environ.get("OLLAMA_HOST", "http://localhost:11434"))
    ap.add_argument("--use_arch_dir", default=str(ROOT_DIR / "DSL" / "blender"))
    ap.add_argument("--use-rag", action="store_true", help="Habilita la inyección de contexto RAG")
    ap.add_argument("--use-agent", action="store_true", help="Habilita la autorreparación de código hasta 3 intentos")
    ap.add_argument("--max-retries", type=int, default=3, help="Intentos máximos del agente")
    args = ap.parse_args()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    prompts = load_prompts(Path(args.prompts))
    outdir = Path(args.outdir); ensure_dir(outdir)
    runner = Path(args.runner)
    if not runner.exists(): raise SystemExit(f"No se encontró {runner}")

    rag_retriever = None
    if args.use_rag:
        if Retriever is None:
            print("ADVERTENCIA: --use-rag activado pero no se encontró ASISTENTE-3D/RAG/retrieval.py. Se omitirá.")
        else:
            print("Cargando base vectorial del RAG...")
            rag_retriever = Retriever(k=3)

    # --- 1) Cargar resumen histórico si existe ---
    summary_json_path = outdir / "results_summary.json"
    summary_csv_path = outdir / "results_summary.csv"
    
    summary = []
    procesados = set()
    
    if summary_json_path.exists():
        try:
            summary = json.loads(summary_json_path.read_text(encoding="utf-8"))
            for entry in summary:
                # Modificamos la clave de procesados para incluir las flags experimentales
                key = f"{entry['model']}_{entry['id']}_rag{entry.get('used_rag',False)}_agt{entry.get('used_agent',False)}"
                procesados.add(key)
        except Exception:
            pass

    cols = ["model","id","titulo","used_rag","used_agent","ollama_ok","compile_ok","rc","chamfer_distance","agent_attempts","execution_error"]

    def guardar_resumen():
        """Guarda tanto el JSON como el CSV de manera segura."""
        summary_json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        lines = [",".join(cols)]
        for r in summary:
            row = [str(r.get(k,"")) for k in cols]
            lines.append(",".join(x.replace("\n"," ").replace(",",";") for x in row))
        summary_csv_path.write_text("\n".join(lines), encoding="utf-8")

    for model in models:
        for item in prompts:
            pid = str(item["id"])
            experiment_key = f"{model}_{pid}_rag{args.use_rag}_agt{args.use_agent}"
            
            if experiment_key in procesados:
                print(f"[SKIP] Ya evaluado: {experiment_key}")
                continue
                
            titulo = item.get("titulo","")
            base_prompt = item["prompt"]
            dificultad = item.get("dificultad", "N/A")
            
            case_dir = outdir / f"{model.replace(':', '_')}_RAG{args.use_rag}_AGT{args.use_agent}" / pid
            ensure_dir(case_dir)

            # RAG Context Injection
            final_prompt = base_prompt
            if args.use_rag and rag_retriever:
                docs = rag_retriever.search(base_prompt)
                context = "\n".join([d.page_content for d in docs])
                final_prompt = f"{base_prompt}\n\n[CONTEXTO DOCUMENTACIÓN DSL]:\n{context}"

            max_attempts = args.max_retries if args.use_agent else 1
            attempt = 0
            success = False
            last_error = ""
            current_prompt = final_prompt
            system_p = SYSTEM_PROMPT
            best_chamfer = None

            while attempt < max_attempts and not success:
                attempt += 1
                try:
                    raw = call_ollama(model, current_prompt, base_url=args.ollama_host, system_prompt=system_p, debug=False)
                except Exception as e:
                    last_error = f"Ollama connection error: {str(e)}"
                    break

                (case_dir/f"llm_raw_att{attempt}.txt").write_text(raw, encoding="utf-8")
                code = extract_code(raw)
                script = case_dir / f"{pid}_script.py"
                script.write_text(code, encoding="utf-8")

                comp_ok, comp_msg = py_compile_file(script)
                (case_dir/f"compile_att{attempt}.log").write_text(comp_msg, encoding="utf-8")
                
                if not comp_ok:
                    last_error = f"Python Syntax Error: {comp_msg}"
                    current_prompt = REPAIR_PROMPT.format(error=last_error)
                    system_p = SYSTEM_PROMPT + "\n\nESTÁS EN MODO REPARACIÓN DE ERRORES SINTÁCTICOS."
                    continue

                env_arch_dir = args.use_arch_dir.strip() or "../DSL/blender"
                gt_script = case_dir / "gt_script.py"
                gt_script.write_text(item.get("python_code", "import blender_arch\n"), encoding="utf-8")
                report = case_dir / f"report_att{attempt}.json"

                rc, out, err = run_blender_runner(BLENDER_BIN, runner, gt_script, script, env_arch_dir, report)
                (case_dir/f"blender_stdout_att{attempt}.log").write_text(out, encoding="utf-8")
                (case_dir/f"blender_stderr_att{attempt}.log").write_text(err, encoding="utf-8")

                rep = {}
                if report.exists():
                    rep = json.loads(report.read_text(encoding="utf-8"))
                    last_error = rep.get("execution_error", "")
                    best_chamfer = rep.get("chamfer_distance", None)

                if rc == 0 and not last_error:
                    success = True
                else:
                    # Preparar iteración del agente si falló Blender
                    blender_full_err = last_error if last_error else err
                    current_prompt = REPAIR_PROMPT.format(error=blender_full_err)
                    system_p = SYSTEM_PROMPT + "\n\nESTÁS EN MODO REPARACIÓN DE ERRORES DE EJECUCIÓN (Runtime)."
            
            summary.append({
                "model": model, "id": pid, "titulo": titulo, "dificultad": dificultad,
                "used_rag": args.use_rag, "used_agent": args.use_agent,
                "ollama_ok": True if attempt > 0 and "Ollama connection error" not in last_error else False,
                "compile_ok": success or ("Python Syntax Error" not in last_error),
                "rc": 0 if success else rc,
                "chamfer_distance": best_chamfer,
                "agent_attempts": attempt,
                "execution_error": last_error if not success else ""
            })
            
            procesados.add(experiment_key)
            guardar_resumen()

    print(f"Listo. Resultados en {outdir}")

if __name__ == "__main__":
    main()
