# generate_dataset_prompts_code_balanced.py
# Genera ítems balanceados (interior/exterior) en tres estilos de código:
#
#   --tier dsl    → código usa blender_arch (DSL del proyecto) — Tier 1
#   --tier bpy    → código usa bpy crudo AEC                  — Tier 2
#   --tier mixed  → mezcla DSL + bpy para casos complejos     — Tier 3
#
# Balance por defecto: 50 % interior, 50 % exterior.
# Usa Gemini (por defecto gemini-2.5-pro) con llamadas paralelas + reintentos.
#
# Requisitos:
#   pip install -U google-generativeai tqdm
#   export GOOGLE_API_KEY="..."
#
# Uso básico:
#   python generate_dataset_prompts_code_balanced.py --total 300 --tier dsl
#   python generate_dataset_prompts_code_balanced.py --total 300 --tier bpy
#   python generate_dataset_prompts_code_balanced.py --total 200 --tier mixed
#
# Para acumular sobre un dataset existente:
#   python generate_dataset_prompts_code_balanced.py --total 400 --tier dsl \
#       --append-to dataset.json --out dataset.json

import os
import re
import json
import time
import math
import argparse
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

import google.generativeai as genai
from tqdm import tqdm


# ---------------------------------------------------------
#  CONFIGURACIÓN GENERAL
# ---------------------------------------------------------

DEFAULT_MODEL      = "gemini-2.5-pro"
MAX_OUTPUT_TOKENS  = 8192
TEMPERATURE        = 0.8
TOP_P              = 0.95
TOP_K              = 64

EDIT_VERBS = [
    r"\bcambia(r|)\b", r"\bmodifica(r|)\b", r"\bajusta(r|)\b",
    r"\baumenta(r|)\b", r"\breduce(r|)\b", r"\bdisminuye(r|)\b",
    r"\bmueve(r|)\b", r"\bdesplaza(r|)\b", r"\bsustituye(r|)\b",
    r"\breemplaza(r|)\b", r"\bsube(r|)\b", r"\bbaja(r|)\b",
    r"\belimina(r|)\b", r"\bborra(r|)\b", r"\bgira(r|)\b",
    r"\brotar\b", r"\brotación\b",
]
EDIT_REGEX = re.compile("|".join(EDIT_VERBS), flags=re.IGNORECASE)

BANNED_SNIPPETS = [
    "bpy.ops.wm.open_mainfile", "bpy.ops.wm.save_mainfile",
    "pip install", "import requests", "subprocess",
    "os.system", "shutil.rmtree",
]


# ---------------------------------------------------------
#  CONTEXTO DEL DSL  (inyectado en los prompts Tier 1 y Tier 3)
# ---------------------------------------------------------

DSL_API_REFERENCE = """
# API blender_arch — referencia rápida
# Importar: import blender_arch as A
# Unidades: metros. Ejes: X=ancho, Y=fondo, Z=alto.

## Materiales
A.asignar_material(obj, nombre="Mat", color=(R,G,B,1))

## Estructurales
A.crear_muro(nombre, largo, alto, grosor=0.2, origen=(0,0,0), rotacion_z=0, material="")
A.crear_columna(nombre, seccion="rect"|"circ", ancho=0.3, fondo=0.3, diametro=0.3, alto=3.0, origen=(0,0,0), material="")
A.crear_losa_rectangular(nombre, ancho, fondo, espesor=0.2, origen=(0,0,0), material="")
A.crear_piso(nombre, ancho, fondo, espesor=0.02, origen=(0,0,0), material="")
A.crear_techo_plano(nombre, ancho, fondo, espesor=0.2, caida_x=0.0, caida_y=0.0, origen=(0,0,0), material="")
A.crear_tejado_dos_aguas(nombre, ancho, fondo, altura_cumbrera=1.5, espesor=0.12, voladizo_x=0.4, voladizo_y=0.4, origen=(0,0,0), material="")

## Huecos
A.crear_ventana(nombre, ancho, alto, prof_marco=0.2, divisiones=(1,1), origen=(0,0,0), material_marco="", material_vidrio="")
A.crear_puerta(nombre, ancho, alto, prof_marco=0.2, origen=(0,0,0), material_panel="", material_marco="")
A.abrir_vanos_batch_rectangulares(muro, centros_world=[(x,y,z),...], ancho, alto)
A.abrir_vanos_grid_local(muro, filas, cols, x0, z0, dx, dz, ancho, alto)

## Escaleras y circulación
A.crear_escalera_recta(nombre, huella=0.28, contrahuella=0.175, ancho=1.2, num_peldanos=14, con_contrahuellas=True, con_zancas=False, espesor_zanca=0.15, origen=(0,0,0), material="")
A.crear_baranda_lineal(nombre, largo, altura=1.05, poste_cada=1.0, num_travesanos=2, origen=(0,0,0), material="")

## Mobiliario
A.crear_mesa(nombre, ancho=1.6, fondo=0.8, alto=0.75, origen=(0,0,0), material="")
A.crear_silla(nombre, origen=(0,0,0), material="")
A.crear_sofa(nombre, ancho=2.2, fondo=0.9, alto_asiento=0.44, origen=(0,0,0), material="")
A.crear_cama(nombre, ancho=1.6, largo=2.0, alto_cabecero=1.1, origen=(0,0,0), material_colchon="", material_estructura="")
A.crear_estanteria(nombre, ancho=1.0, alto=2.1, fondo=0.3, num_estantes=4, con_fondo=True, origen=(0,0,0), material="")
A.crear_armario(nombre, ancho=2.0, alto=2.4, fondo=0.6, num_puertas=2, con_zocalo=True, origen=(0,0,0), material="")

## Exterior
A.crear_terreno_plano(nombre, ancho, fondo, espesor=0.3, origen=(0,0,0), material="")
A.crear_arbol_simple(nombre, radio_copa=1.5, altura_copa=3.0, altura_tronco=1.5, origen=(0,0,0))

## Composites de alto nivel
A.crear_habitacion(nombre, ancho, fondo, alto, grosor_muro=0.2, grosor_losa=0.2, con_suelo=True, con_techo=True, origen=(0,0,0), material_muro="", material_suelo="", material_techo="")
A.crear_casa_n_pisos(nombre, pisos=2, ancho=10.0, fondo=8.0, alto_piso=2.8, grosor_muro=0.2, con_tejado=True, altura_cumbrera=1.5, voladizo=0.4, origen=(0,0,0), material_muro="", material_losa="", material_tejado="")
A.crear_edificio_n_pisos(nombre, pisos=4, ancho=12.0, fondo=15.0, alto_piso=2.8, grosor_muro=0.2, con_techo_plano=True, con_columnas=False, dim_columna=0.3, modulo_columna_x=4.0, modulo_columna_y=5.0, ventanas_fachada=True, ventana_ancho=1.2, ventana_alto=1.1, ventana_alfeizar=0.9, ventana_separacion=2.4, origen=(0,0,0), material_fachada="", material_losa="", material_vidrio="", material_marco="")

## Geometría genérica
A.extruir_perfil(nombre, puntos_2d=[(x,y),...], altura=3.0, material="")
A.extruir_con_huecos(nombre, contorno=[(x,y),...], agujeros=[[(x,y),...]], altura=0.1, material="")
A.crear_tuberia(nombre, puntos_3d=[(x,y,z),...], radio=0.025, material="")

## Iluminación y cámara
A.agregar_luz(nombre, tipo="POINT"|"SUN"|"AREA"|"SPOT", ubicacion=(0,0,3), energia=400, color=(1,1,1))
A.crear_camara(nombre, ubicacion=(0,-10,5), rotacion=(60,0,0), tipo="PERSP"|"ORTHO", focal_length=35, activa=True)

## Utilidades
A.anclar_a(obj_mobile, obj_anchor, punto_anchor="frente"|"detras"|"izquierda"|"derecha"|"encima", offset=(0,0,0))
A.limpiar_escena()
A.exportar_escena(ruta, formato="BLEND"|"OBJ"|"FBX"|"GLTF"|"STL")
A.validar_malla(obj, verbose=True)

## Materiales disponibles (ejemplos)
Estructurales: Hormigon, Ladrillo, Ladrillo_Rojo, Acero, Acero_Inox
Muros/cielos:  Muro_Pintura, Muro_Pintura_Gris, Estuco, Yeso
Pisos:         Parquet, Ceramica_Piso, Porcelanato, Concreto_Piso, Cesped
Cubiertas:     Teja, Teja_Zinc, Membrana_Imperm
Madera:        Madera, Madera_Roble, Madera_Nogal, MDF_Blanco
Vidrio:        Vidrio, Vidrio_Templado, Vidrio_Esmerilado
Marcos:        Marco_Blanco, Marco_Aluminio, Marco_Negro
Textiles:      Tela_Gris, Tela_Beige, Cuero, Textil_Blanco
Metales:       Cobre, Bronce, Metal
Exterior:      Terreno, Asfalto, Agua
"""


# ---------------------------------------------------------
#  INSTRUCCIONES POR TIER
# ---------------------------------------------------------

SYSTEM_INSTRUCTIONS = {
    "dsl": (
        "Eres un arquitecto computacional experto en Blender y en el DSL blender_arch. "
        "Produces ítems de CREACIÓN (no edición) en ESPAÑOL para el dominio AEC. "
        "El código SIEMPRE usa 'import blender_arch as A' y llama exclusivamente "
        "a las funciones del DSL. El código debe ser autocontenido y ejecutable "
        "en Blender sin dependencias externas adicionales."
    ),
    "bpy": (
        "Eres un arquitecto y diseñador computacional experto en Blender (bpy). "
        "Produces ítems de CREACIÓN (no edición) en ESPAÑOL para el dominio AEC. "
        "El código usa 'import bpy' y la API nativa de Blender. "
        "El código debe ser autocontenido y ejecutable en Blender."
    ),
    "mixed": (
        "Eres un arquitecto computacional experto en Blender y en el DSL blender_arch. "
        "Produces ítems de CREACIÓN complejos en ESPAÑOL para el dominio AEC. "
        "El código combina 'import blender_arch as A' para elementos estándar "
        "e 'import bpy' directamente para geometría o lógica que el DSL no cubre. "
        "El código debe ser autocontenido y ejecutable en Blender."
    ),
}

BATCH_TEMPLATES = {
    "dsl": """
Genera exactamente {count} ítems para el dominio: {fixed_domain}.
Usa SOLO las funciones del DSL blender_arch (ver API abajo). SOLO CREACIÓN (no edición).
Varía categorías y complejidad. Mezcla elementos simples (una función) y compuestos
(crear_habitacion, crear_casa_n_pisos, crear_edificio_n_pisos + mobiliario).

{dsl_api}

POLÍTICAS:
- Escena limpia: empieza con A.limpiar_escena() o bpy.ops.wm.read_homefile(use_empty=True)
- Unidades métricas, dimensiones realistas (ver estándares AEC).
- Relaciones espaciales coherentes: muebles sobre el suelo, columnas alineadas, etc.
- Si hay varias funciones, las posiciones deben ser consistentes entre sí.
- No inventar funciones que no existan en el API.

{style_and_spatial}
""",
    "bpy": """
Genera exactamente {count} ítems para el dominio: {fixed_domain}. SOLO CREACIÓN.
Usa la API nativa de Blender (import bpy). Código AEC: muros, losas, fachadas,
cubiertas, mobiliario, jardines, elementos urbanos. Varía categorías y complejidad.

{style_and_spatial}
""",
    "mixed": """
Genera exactamente {count} ítems COMPLEJOS para el dominio: {fixed_domain}. SOLO CREACIÓN.
Combina funciones del DSL blender_arch (para elementos estándar) con bpy directo
(para geometría personalizada, modificadores o lógica que el DSL no cubre).
Complejidad media-alta. Escenas con múltiples elementos relacionados.

{dsl_api}

{style_and_spatial}
""",
}

STYLE_AND_SPATIAL_POLICY = """
REQUISITOS ESTRICTOS:
- Configura unidades métricas. Blender es Z-up.
- No uses red ni librerías externas. No instales paquetes.
- No abras/guardes archivos .blend del usuario.
- Relaciones espaciales:
  * 2 paredes: contiguas y ortogonales (esquina).
  * 4 paredes: cuarto rectangular cerrado coherente.
  * Muebles: sobre el piso, separados de los muros, bien distribuidos.
  * Si hay relaciones ("centrado", "junto a", "alineado"), respétalas.
- Dimensiones realistas en metros.
- Código con comentarios mínimos y nombres descriptivos de variables.
- Complejidad variada: low (1 elemento), medium (2-4 elementos), high (escena completa).

FORMATO DE SALIDA (JSON array estricto):
Devuelve EXCLUSIVAMENTE un JSON array. Cada objeto:
- "domain":      "{fixed_domain}"
- "category":    string corta (muro / losa / ventana / escalera / habitacion / casa / mobiliario / fachada / jardin ...)
- "complexity":  "low" | "medium" | "high"
- "tier":        "{tier}"
- "prompt":      en español, comienza con verbo de creación (Crea/Construye/Modela/Genera/Levanta/Diseña)
- "python_code": código Python autocontenido, SIN backticks
"""

EXAMPLE_ITEMS = {
    "dsl": """
EJEMPLO (no repetir literal):
{
  "domain": "interior",
  "category": "habitacion",
  "complexity": "medium",
  "tier": "dsl",
  "prompt": "Diseña una habitación de 5 x 4 m con piso de parquet y techo de hormigón, con una ventana de 1.2 x 1.0 m en la fachada sur.",
  "python_code": "import blender_arch as A\\nA.limpiar_escena()\\nhab = A.crear_habitacion('Dormitorio', ancho=5.0, fondo=4.0, alto=2.8, material_muro='Muro_Pintura', material_suelo='Parquet', material_techo='Hormigon')\\nA.crear_ventana('V_Sur', ancho=1.2, alto=1.0, prof_marco=0.2, origen=(1.9, 0, 0.9), material_vidrio='Vidrio', material_marco='Marco_Blanco')"
}
""",
    "bpy": """
EJEMPLO (no repetir literal):
{
  "domain": "interior",
  "category": "mesa",
  "complexity": "medium",
  "tier": "bpy",
  "prompt": "Crea una mesa de comedor rectangular de 2.0 x 1.0 m y 0.75 m de alto, centrada en la sala principal.",
  "python_code": "import bpy\\nbpy.ops.wm.read_homefile(use_empty=True)\\nbpy.context.scene.unit_settings.system = 'METRIC'\\nbpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.375))\\nmesa = bpy.context.active_object\\nmesa.name = 'Mesa_Comedor'\\nmesa.scale = (2.0, 1.0, 0.75)\\nbpy.ops.object.transform_apply(scale=True)"
}
""",
    "mixed": """
EJEMPLO (no repetir literal):
{
  "domain": "exterior",
  "category": "fachada_detalle",
  "complexity": "high",
  "tier": "mixed",
  "prompt": "Construye la fachada principal de una casa de 2 pisos con terreno, tres árboles y una reja metálica de barrotes personalizados en la entrada.",
  "python_code": "import blender_arch as A\\nimport bpy\\nfrom math import pi\\nA.limpiar_escena()\\nA.crear_terreno_plano('Terreno', ancho=14, fondo=10, espesor=0.3, origen=(-2,-1,-0.3))\\nA.crear_casa_n_pisos('Casa', pisos=2, ancho=10, fondo=8, alto_piso=2.8, con_tejado=True, material_muro='Ladrillo_Rojo')\\nfor i, x in enumerate([-1.5, 11.5]):\\n    A.crear_arbol_simple(f'Arbol_{i}', radio_copa=1.5, altura_tronco=1.5, origen=(x, 3, 0))\\n# Reja de barrotes con bpy\\nfor k in range(7):\\n    bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=1.2, location=(-0.5 + k*0.35, -0.5, 0.6))\\n    bpy.context.active_object.name = f'Barrote_{k}'"
}
""",
}


# ---------------------------------------------------------
#  UTILIDADES
# ---------------------------------------------------------

def is_creation_prompt(txt: str) -> bool:
    return bool(txt) and EDIT_REGEX.search(txt) is None

def extract_first_json_array(text: str):
    m = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.DOTALL | re.IGNORECASE)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except Exception:
            pass
    m2 = re.search(r"(\[.*\])", text, re.DOTALL)
    if m2:
        try:
            return json.loads(m2.group(1).strip())
        except Exception:
            pass
    try:
        return json.loads(text)
    except Exception:
        return None

def backoff_sleep(attempt: int, base: float = 1.0, max_sleep: float = 30.0):
    time.sleep(min(max_sleep, base * (2 ** attempt) + 0.2 * attempt))

def dedup_by_prompt(items: list) -> list:
    seen, out = set(), []
    for it in items:
        key = re.sub(r"\s+", " ", it["prompt"].strip().lower())
        if key not in seen:
            seen.add(key)
            out.append(it)
    return out


# ---------------------------------------------------------
#  CONSTRUCCIÓN DEL PROMPT POR TIER
# ---------------------------------------------------------

def build_user_prompt(batch_size: int, fixed_domain: str, tier: str) -> str:
    spatial = STYLE_AND_SPATIAL_POLICY.replace("{fixed_domain}", fixed_domain).replace("{tier}", tier)
    template = BATCH_TEMPLATES[tier]
    prompt = template.format(
        count=batch_size,
        fixed_domain=fixed_domain,
        dsl_api=DSL_API_REFERENCE if tier in ("dsl", "mixed") else "",
        style_and_spatial=spatial,
    )
    prompt += EXAMPLE_ITEMS[tier]
    prompt += "\nDevuelve SOLO el JSON array."
    return prompt


# ---------------------------------------------------------
#  LLAMADA A GEMINI
# ---------------------------------------------------------

def call_gemini_batch(model_name: str, system_instruction: str, user_prompt: str,
                      retries: int = 5) -> list:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Falta GOOGLE_API_KEY en el entorno.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_instruction,
        generation_config={
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "top_k": TOP_K,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "response_mime_type": "application/json",
        },
    )

    last_err = None
    for attempt in range(retries):
        try:
            resp = model.generate_content(user_prompt)
            text = resp.text if hasattr(resp, "text") else str(resp)
            data = extract_first_json_array(text)
            if not isinstance(data, list):
                raise ValueError("Respuesta sin JSON array válido.")
            return data
        except Exception as e:
            last_err = e
            backoff_sleep(attempt)
    raise RuntimeError(f"Gemini falló tras {retries} reintentos: {last_err}")


# ---------------------------------------------------------
#  SANITIZACIÓN POR TIER
# ---------------------------------------------------------

def sanitize_item(it: dict, forced_domain: str, tier: str) -> dict | None:
    domain     = "interior" if forced_domain == "interior" else "exterior"
    category   = str(it.get("category", "")).strip() or "general"
    complexity = str(it.get("complexity", "")).strip().lower()
    prompt     = str(it.get("prompt", "")).strip()
    code       = str(it.get("python_code", "")).strip()

    if not prompt or not code:
        return None
    if not is_creation_prompt(prompt):
        return None
    if complexity not in {"low", "medium", "high"}:
        complexity = "medium"
    if any(b in code for b in BANNED_SNIPPETS):
        return None

    code = code.replace("```", "")

    # Validación de imports según tier
    has_bpy     = "import bpy" in code
    has_dsl     = "import blender_arch" in code

    if tier == "dsl" and not has_dsl:
        return None
    if tier == "bpy" and not has_bpy:
        return None
    if tier == "mixed" and not (has_dsl or has_bpy):
        return None

    # Heurística mínima: el código crea algo
    creates_dsl = any(f"A.crear_" in code or f"A.extruir_" in code
                      or f"A.agregar_" in code for _ in [1])
    creates_bpy = ("bpy.ops.mesh." in code or "bpy.data.objects.new" in code
                   or ("bpy.ops.object" in code and "add" in code)
                   or "bpy.ops.curve." in code)

    if tier == "dsl"   and not creates_dsl:
        return None
    if tier == "bpy"   and not creates_bpy:
        return None
    if tier == "mixed" and not (creates_dsl or creates_bpy):
        return None

    return {
        "domain":      domain,
        "category":    category,
        "complexity":  complexity,
        "tier":        tier,
        "prompt":      prompt,
        "python_code": code,
    }


# ---------------------------------------------------------
#  GENERACIÓN PARA UN DOMINIO
# ---------------------------------------------------------

def generate_for_domain(target_count: int, fixed_domain: str, tier: str,
                        batch_size: int, concurrency: int, model: str,
                        max_rounds: int = 8) -> list:
    collected = []
    rounds    = 0
    system    = SYSTEM_INSTRUCTIONS[tier]

    while len(collected) < target_count and rounds < max_rounds:
        rounds += 1
        remaining = target_count - len(collected)
        n_batches = max(1, math.ceil(remaining / batch_size))
        prompts   = [build_user_prompt(batch_size, fixed_domain, tier)
                     for _ in range(n_batches)]

        raw_items = []
        with ThreadPoolExecutor(max_workers=concurrency) as ex:
            futures = [ex.submit(call_gemini_batch, model, system, p)
                       for p in prompts]
            for fut in tqdm(as_completed(futures), total=len(futures),
                            desc=f"[{tier}] {fixed_domain} ronda {rounds}"):
                try:
                    raw_items.extend(fut.result())
                except Exception as e:
                    print(f"  [WARN] Lote fallido: {e}")

        sanitized = [s for it in raw_items
                     if (s := sanitize_item(it, fixed_domain, tier))]
        collected.extend(sanitized)
        collected = dedup_by_prompt(collected)
        print(f"  → {len(collected)}/{target_count} válidos acumulados")

    return collected[:target_count]


# ---------------------------------------------------------
#  MAIN
# ---------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Genera dataset AEC para fine-tuning (DSL / bpy / mixed)."
    )
    ap.add_argument("--total",       type=int,   default=300,
                    help="Total de ítems a generar (debe ser par).")
    ap.add_argument("--tier",        type=str,   default="dsl",
                    choices=["dsl", "bpy", "mixed"],
                    help="Estilo de código: dsl | bpy | mixed.")
    ap.add_argument("--batch-size",  type=int,   default=10,
                    help="Ítems por llamada al modelo.")
    ap.add_argument("--concurrency", type=int,   default=6,
                    help="Llamadas concurrentes a Gemini.")
    ap.add_argument("--model",       type=str,   default=DEFAULT_MODEL,
                    help="Modelo Gemini a usar.")
    ap.add_argument("--out",         type=str,   default=None,
                    help="Archivo JSON de salida. Por defecto: dataset_<tier>.json")
    ap.add_argument("--append-to",   type=str,   default=None,
                    help="Archivo JSON existente al que acumular nuevos ítems.")
    args = ap.parse_args()

    if args.total % 2 != 0:
        raise SystemExit("--total debe ser par (balance 50/50 interior/exterior).")
    if not os.environ.get("GOOGLE_API_KEY"):
        raise SystemExit("Falta variable de entorno GOOGLE_API_KEY.")

    out_file = args.out or f"dataset_{args.tier}.json"
    half     = args.total // 2

    print(f"\n[INFO] Tier: {args.tier} | {half} interior + {half} exterior | modelo: {args.model}")

    interior = generate_for_domain(half, "interior", args.tier,
                                   args.batch_size, args.concurrency, args.model)
    exterior = generate_for_domain(half, "exterior", args.tier,
                                   args.batch_size, args.concurrency, args.model)

    new_items = interior + exterior

    # ── Acumular sobre dataset existente si se pide ───────────────────────
    existing_items: dict = {}
    if args.append_to:
        try:
            with open(args.append_to, encoding="utf-8") as f:
                existing = json.load(f)
            existing_items = existing.get("items", {})
            print(f"[INFO] Acumulando sobre {len(existing_items)} ítems existentes.")
        except FileNotFoundError:
            print(f"[WARN] No se encontró {args.append_to}, creando archivo nuevo.")

    # Asignar IDs consecutivos desde el último existente
    last_id = 0
    if existing_items:
        nums = [int(k[1:]) for k in existing_items if k.startswith("p") and k[1:].isdigit()]
        last_id = max(nums) if nums else 0

    for i, item in enumerate(new_items, start=last_id + 1):
        existing_items[f"p{i:04d}"] = item

    # Estadísticas
    tiers_count   = {}
    domains_count = {}
    for it in existing_items.values():
        tiers_count[it.get("tier", "?")] = tiers_count.get(it.get("tier", "?"), 0) + 1
        domains_count[it.get("domain", "?")] = domains_count.get(it.get("domain", "?"), 0) + 1

    out_obj = {
        "meta": {
            "updated_at":   datetime.now(timezone.utc).isoformat(),
            "model":        args.model,
            "language":     "es",
            "type":         "creation+code",
            "total":        len(existing_items),
            "tiers":        tiers_count,
            "balance":      domains_count,
        },
        "items": existing_items,
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(out_obj, f, ensure_ascii=False, indent=2)

    print(f"""
[OK] {len(new_items)} ítems nuevos generados.
     Total en archivo: {len(existing_items)}
     Tiers: {tiers_count}
     Balance: {domains_count}
     Guardado en: {out_file}
""")


if __name__ == "__main__":
    main()
