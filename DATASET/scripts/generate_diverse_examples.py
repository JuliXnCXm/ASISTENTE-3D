# generate_diverse_examples.py
#
# Genera ejemplos temáticos específicos para cubrir los gaps de diversidad
# del dataset de creación AEC. Cada tema tiene un prompt especializado
# que guía a Gemini hacia categorías concretas y programas arquitectónicos reales.
#
# Uso:
#   python generate_diverse_examples.py --theme casas_programa --total 60
#   python generate_diverse_examples.py --theme apartamentos --total 50
#   python generate_diverse_examples.py --all --append-to dataset_v2_with_blends_with_depth.json
#
# Temas disponibles:
#   casas_programa       - Casas con programa interior (sala+cocina+dormitorio, etc.)
#   apartamentos         - Studios, 1BD, 2BD con distribución real
#   interiores_esp       - Cocinas, baños, suites, oficinas home con detalle
#   espacios_colectivos  - Lobby, cafetería, tienda, recepción, sala de espera
#   fachadas_modernas    - Fachadas contemporáneas (no tejado a dos aguas)
#   exterior_diverso     - Plazas urbanas, patios de diseño, jardines modernos

import os, re, json, time, math, argparse
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

import google.generativeai as genai
from tqdm import tqdm


# ---------------------------------------------------------
#  CONFIG
# ---------------------------------------------------------

DEFAULT_MODEL     = "gemini-2.5-pro"
MAX_OUTPUT_TOKENS = 65536
TEMPERATURE       = 0.85
TOP_P             = 0.95

BANNED_SNIPPETS = [
    "bpy.ops.wm.open_mainfile", "bpy.ops.wm.save_mainfile",
    "pip install", "import requests", "subprocess",
    "os.system", "shutil.rmtree",
]

EDIT_REGEX = re.compile(
    r"\b(cambia(r)?|modifica(r)?|ajusta(r)?|aumenta(r)?|reduce(r)?"
    r"|disminuye(r)?|mueve(r)?|desplaza(r)?|sustituye(r)?|reemplaza(r)?"
    r"|elimina(r)?|borra(r)?|gira(r)?|rotar|rotación)\b",
    flags=re.IGNORECASE
)


# ---------------------------------------------------------
#  DSL API REFERENCE
# ---------------------------------------------------------

DSL_API = """
# API blender_arch — referencia rápida
# Importar: import blender_arch as A
# Unidades: metros. Ejes: X=ancho, Y=fondo, Z=alto.

## Materiales
A.asignar_material(obj, nombre="Mat", base_color=(R,G,B,1.0))

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
A.crear_escalera_recta(nombre, huella=0.28, contrahuella=0.175, ancho=1.2, num_peldanos=14, con_contrahuellas=True, con_zancas=False, origen=(0,0,0), material="")
A.crear_baranda_lineal(nombre, largo, altura=1.05, poste_cada=1.0, num_travesanos=2, origen=(0,0,0), material="")

## Mobiliario
A.crear_mesa(nombre, ancho=1.6, fondo=0.8, alto=0.75, origen=(0,0,0), material_tablero="Madera", material_patas="Metal")
A.crear_silla(nombre, ancho=0.45, fondo=0.45, alto_asiento=0.45, alto_respaldo=0.9, origen=(0,0,0), material="Madera")
A.crear_sofa(nombre, ancho=2.0, fondo=0.9, alto_asiento=0.45, origen=(0,0,0), material="Tela", material_estructura="Madera")
A.crear_cama(nombre, ancho=1.6, largo=2.0, alto_cabecero=1.0, origen=(0,0,0), material_base="Madera", material_colchon="Textil")
A.crear_estanteria(nombre, ancho=1.2, alto=2.0, fondo=0.35, num_estantes=5, con_fondo=True, origen=(0,0,0), material="Madera")
A.crear_armario(nombre, ancho=2.0, alto=2.4, fondo=0.6, num_puertas=2, con_zocalo=True, origen=(0,0,0), material_cuerpo="Madera", material_puerta="Madera_Lacada")

## Exterior
A.crear_terreno_plano(nombre, ancho, fondo, espesor=0.3, origen=(0,0,0), material="")
A.crear_arbol_simple(nombre, radio_copa=1.5, altura_copa=3.0, altura_tronco=1.5, origen=(0,0,0))

## Composites de alto nivel
A.crear_habitacion(nombre, ancho, fondo, alto, grosor_muro=0.2, grosor_losa=0.2, con_suelo=True, con_techo=True, origen=(0,0,0), material_muro="", material_suelo="", material_techo="")
A.crear_casa_n_pisos(nombre, pisos=2, ancho=10.0, fondo=8.0, alto_piso=2.8, grosor_muro=0.2, con_tejado=True, altura_cumbrera=1.5, voladizo=0.4, origen=(0,0,0), material_muro="", material_losa="", material_tejado="")
A.crear_edificio_n_pisos(nombre, pisos=4, ancho=12.0, fondo=15.0, alto_piso=2.8, grosor_muro=0.2, con_techo_plano=True, con_columnas=False, dim_columna=0.3, modulo_columna_x=4.0, modulo_columna_y=5.0, ventanas_fachada=True, ventana_ancho=1.2, ventana_alto=1.1, ventana_alfeizar=0.9, ventana_separacion=2.4, origen=(0,0,0), material_fachada="", material_losa="", material_vidrio="", material_marco="")

## Geometría genérica
A.extruir_perfil(nombre, puntos_2d=[(x,y),...], altura=3.0, cerrar_perfil=True, material="Generic")
A.extruir_con_huecos(nombre, contorno=[(x,y),...], agujeros=[[(x,y),...]], altura=0.1, material="")
A.crear_tuberia(nombre, puntos_3d=[(x,y,z),...], radio=0.025, material="")

## Iluminación y cámara
A.agregar_luz(nombre, tipo="POINT"|"SUN"|"AREA"|"SPOT", ubicacion=(0,0,3), energia=400, color=(1,1,1))
A.crear_camara(nombre, ubicacion=(0,-10,5), rotacion=(60,0,0), tipo="PERSP"|"ORTHO", focal_length=35, activa=True)

## Utilidades
A.anclar_a(obj_mobile, obj_anchor, punto_anchor="frente"|"detras"|"izquierda"|"derecha"|"encima", offset=(0,0,0))
A.limpiar_escena()

## Materiales disponibles
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
#  TEMAS — cada uno define el tipo de ejemplos a generar
# ---------------------------------------------------------

THEMES = {

    "casas_programa": {
        "domain": "interior",
        "tier": "mixed",
        "category_hint": "casa",
        "description": """
Genera viviendas unifamiliares con PROGRAMA ARQUITECTÓNICO REAL.
NO generes casas genéricas — cada ejemplo debe especificar zonificación funcional.

Tipologías y programas a cubrir (varía entre ellos):
- Casa de 45–60 m²: sala-comedor integrado + cocina + 1 dormitorio + baño
- Casa de 60–80 m²: sala + comedor separado + cocina + 2 dormitorios + baño + lavadero
- Casa de 80–100 m²: zona diurna (sala+comedor+cocina abierta) + zona nocturna (2-3 dorm + 2 baños)
- Casa de 100–120 m²: sala de estar + sala de TV + cocina con isla + comedor + 3 dorm + 2 baños + patio
- Casa en L o U: patio central, galería de circulación
- Casa tipo dúplex: planta baja social, planta alta privada, escalera interior
- Casa patio: habitaciones alrededor de un patio central descubierto
- Cabaña/casa de campo compacta: programa abierto, techo inclinado, porche

IMPORTANTE: Los prompts deben mencionar el programa (qué espacios hay y cómo se relacionan).
El código debe modelar los muros, losas y al menos el mobiliario clave de cada zona.
Mezcla tier DSL y bpy según lo que sea más adecuado para la complejidad.
""",
    },

    "apartamentos": {
        "domain": "interior",
        "tier": "mixed",
        "category_hint": "apartamento",
        "description": """
Genera apartamentos/viviendas colectivas con programa real y distribución funcional.

Tipologías a cubrir (varía entre ellas):
- Monoambiente/estudio 25–35 m²: cama + zona trabajo + kitchenette + baño, todo integrado
- Apartamento 1 dormitorio 40–55 m²: sala-comedor + cocina + dormitorio + baño
- Apartamento 2 dormitorios 60–75 m²: sala + comedor + cocina + 2 dormitorios + 1-2 baños
- Apartamento 3 dormitorios 80–95 m²: sala + comedor + cocina + 3 dorm + 2 baños + balcón
- Loft industrial 50–70 m²: planta abierta, zona trabajo + zona descanso, alturas dobles
- Dúplex 70–90 m²: 2 plantas, escalera interior, social abajo, privado arriba
- Apartamento para adultos mayores: accesible, sin escaleras, baño adaptado, cocina amplia
- Apartamento compartido: 3-4 dormitorios privados + zonas comunes (sala, cocina, baños)

Los prompts deben describir la distribución y las relaciones espaciales.
El código debe modelar los muros divisorios y el mobiliario principal de cada zona.
""",
    },

    "interiores_esp": {
        "domain": "interior",
        "tier": "mixed",
        "category_hint": "cocina|baño|dormitorio|oficina",
        "description": """
Genera espacios interiores especializados con detalle funcional y mobiliario específico.
VARÍA entre estas 4 categorías:

--- COCINAS (25% de los items) ---
- Cocina en línea recta: módulos altos + bajos, encimera, extractor
- Cocina en L: módulos en dos paredes perpendiculares, esquinera
- Cocina en U: tres paredes, isla opcional, espacio de trabajo amplio
- Cocina con isla central: isla de 2×1m, taburetes, encimera en isla
- Cocina abierta integrada a sala: barra americana, divisor visual

--- BAÑOS (25% de los items) ---
- Baño completo con ducha: inodoro + lavabo + ducha con plato
- Baño con bañera exenta: bañera de pie + ducha + doble lavabo
- Baño adaptado/accesible: ducha nivel suelo, barras de apoyo, espacio de maniobra
- Baño pequeño (2×1.5m): compacto, ducha, inodoro, lavabo
- Baño en suite: integrado al dormitorio, separación por tabique bajo o vidrio

--- DORMITORIOS (25% de los items) ---
- Dormitorio principal suite 4×4m: cama king + armario a medida + zona lectura + baño en suite
- Dormitorio infantil 3×3m: cama individual + escritorio + estantería + zona de juegos
- Dormitorio juvenil: cama + escritorio + armario + estantería de libros
- Dormitorio de invitados: cama doble + mesitas + armario pequeño

--- OFICINAS (25% de los items) ---
- Home office compacto: escritorio en L + silla + estantería + luz cenital
- Oficina open plan 8×6m: 4 puestos de trabajo + sala reuniones separada por tabique vidrio
- Despacho privado 4×3m: escritorio ejecutivo + silla + librería + sillón visita
- Sala de reuniones: mesa rectangular + 8 sillas + pantalla en pared

El código debe modelar el mobiliario específico de cada espacio con dimensiones reales.
""",
    },

    "espacios_colectivos": {
        "domain": "interior",
        "tier": "mixed",
        "category_hint": "comercial|lobby|cafeteria|recepcion",
        "description": """
Genera espacios de uso colectivo/comercial para el dominio AEC.
VARÍA entre estos tipos:

- Lobby de edificio de oficinas: recepción con mostrador + zona de espera + acceso a ascensores
- Recepción de hotel pequeño: mostrador largo + zona lounge + iluminación ambiental
- Cafetería urbana 40 m²: barra + 5 mesas de 4 personas + zona de espera + mostrador
- Restaurante pequeño 60 m²: 8 mesas + zona de barra + acceso a cocina
- Tienda de ropa 50 m²: probadores + percheros + mostrador de caja + escaparate
- Sala de espera médica: 8 sillas en L + mostrador de recepción + zona infantil
- Aula de clases 9×7m: 20 pupitres + escritorio docente + pizarrón + proyector
- Sala de coworking: 6 puestos individuales + 1 mesa colaborativa + kitchenette + baños
- Biblioteca pequeña: estanterías perimetrales + 4 mesas de lectura + zona infantil

Prompts en español con verbo de creación. Código con mobiliario característico y dimensiones reales.
""",
    },

    "fachadas_modernas": {
        "domain": "exterior",
        "tier": "mixed",
        "category_hint": "fachada",
        "description": """
Genera fachadas arquitectónicas CONTEMPORÁNEAS.
PROHIBIDO usar tejado a dos aguas — usa cubiertas planas, inclinadas de un agua, o planas ajardinadas.

Tipologías a cubrir:
- Fachada minimalista: muro de hormigón liso + ventanas de piso a techo + cubierta plana
- Fachada con celosía: muro base + celosía de lamas verticales o horizontales como filtro solar
- Fachada de vidrio: muro cortina de vidrio templado + estructura metálica
- Fachada industrial: ladrillo visto + ventanas industriales de hierro + cubierta metálica
- Fachada con terraza en voladizo: losa en voladizo 1.5–2m + barandilla + jardineras
- Fachada bioclimática: aleros de protección solar + ventanas operable + vegetación vertical
- Fachada con piel de madera: revestimiento de listones de madera + ventanas ocultas en carpintería
- Fachada comercial: escaparate de vidrio + letrero + toldo + acceso amplio
- Fachada de edificio de apartamentos: módulo repetitivo de balcones + ventanas + barandillas

Cada ejemplo debe incluir la fachada completa (muros, huecos, cubierta, elementos complementarios).
Usa DSL para los muros base y bpy para elementos de detalle (celosía, lamas, barandillas personalizadas).
""",
    },

    "exterior_diverso": {
        "domain": "exterior",
        "tier": "mixed",
        "category_hint": "plaza|patio|jardin|paisaje",
        "description": """
Genera espacios exteriores urbanos y paisajísticos DIVERSOS.
NO generes casas con césped y árboles — eso ya está cubierto.

Tipos a cubrir:
- Plaza urbana dura: pavimento de hormigón o adoquín + bancas + farolas + árbol en alcorque
- Patio interior de edificio: área pavimentada + jardín en borde + banco corrido + árbol central
- Jardín de diseño contemporáneo: camino sinuoso + zonas de vegetación + pérgola + estanque
- Terraza ajardinada en azotea: cubierta plana + deck de madera + jardineras perimetrales + pérgola
- Parque lineal: camino peatonal + zonas de descanso + juegos infantiles + iluminación
- Patio de colegio: zona de juegos + área de descanso + árbol de sombra + bancas
- Área de barbacoa exterior: parrilla + mesa + pérgola + piso de deck
- Jardín zen: grava rastrillada + rocas + bambú + camino de piedra + fuente
- Estacionamiento con paisajismo: plaza de parking + separadores verdes + árboles de sombra
- Acceso monumental a edificio: escalinata + rampas + jardineras + iluminación de piso

Usa DSL para terrenos y mobiliario urbano, bpy para elementos de detalle (pavimentos, caminos, bancas personalizadas).
""",
    },
}


# ---------------------------------------------------------
#  FORMATO DE SALIDA Y POLÍTICAS
# ---------------------------------------------------------

OUTPUT_FORMAT = """
POLÍTICAS OBLIGATORIAS:
- SOLO CREACIÓN (sin edición). Prompts comienzan con: Crea/Construye/Modela/Genera/Levanta/Diseña
- Escena limpia: A.limpiar_escena() o bpy.ops.wm.read_homefile(use_empty=True)
- Unidades métricas, dimensiones AEC reales. No inventar funciones DSL que no existan.
- Relaciones espaciales coherentes: muebles sobre el suelo, separados de muros 0.05–0.2m
- No usar red, pip, subprocess ni guardar/abrir archivos .blend
- asignar_material SIEMPRE requiere un objeto como primer argumento: A.asignar_material(obj, nombre="Mat", base_color=(R,G,B,1.0))
  NO usar como fábrica de materiales: mat = A.asignar_material(...) es INCORRECTO
- Usar SOLO funciones que existen en la API. No inventar A.crear_cocina(), A.crear_bano(), A.crear_habitacion_completa(), etc.

FORMATO DE SALIDA (JSON array estricto, sin texto adicional):
Cada objeto del array:
- "domain":      "interior" | "exterior"
- "category":    categoría corta descriptiva (casa, apartamento, cocina, baño, fachada, plaza, etc.)
- "complexity":  "low" | "medium" | "high"
- "tier":        "dsl" | "bpy" | "mixed"
- "prompt":      en español, comienza con verbo de creación, describe el PROGRAMA y los espacios
- "python_code": código Python autocontenido, SIN backticks ni bloques markdown

Devuelve SOLO el JSON array.
"""


# ---------------------------------------------------------
#  INFRAESTRUCTURA GEMINI
# ---------------------------------------------------------

def extract_json_array(text: str):
    for pat in [
        r"```(?:json)?\s*(\[.*?\])\s*```",
        r"(\[.*\])",
    ]:
        m = re.search(pat, text, re.DOTALL | re.IGNORECASE)
        if m:
            try:
                return json.loads(m.group(1).strip())
            except Exception:
                pass
    try:
        return json.loads(text)
    except Exception:
        return None


def backoff(attempt: int):
    time.sleep(min(30.0, 1.0 * (2 ** attempt)))


def call_gemini(model_name: str, system: str, user: str, retries: int = 5) -> list:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Falta GOOGLE_API_KEY")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system,
        generation_config={
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "response_mime_type": "application/json",
        },
    )

    for attempt in range(retries):
        try:
            resp = model.generate_content(user)
            text = resp.text if hasattr(resp, "text") else str(resp)
            data = extract_json_array(text)
            if not isinstance(data, list):
                raise ValueError("Sin JSON array válido")
            return data
        except Exception as e:
            if attempt == retries - 1:
                raise RuntimeError(f"Gemini falló: {e}")
            backoff(attempt)
    return []


# ---------------------------------------------------------
#  SANITIZACIÓN
# ---------------------------------------------------------

def sanitize(it: dict, theme: dict) -> dict | None:
    prompt = str(it.get("prompt", "")).strip()
    code   = str(it.get("python_code", "")).strip()
    if not prompt or not code:
        return None
    if EDIT_REGEX.search(prompt):
        return None
    if any(b in code for b in BANNED_SNIPPETS):
        return None

    code = code.replace("```", "").strip()

    # Debe tener algún import válido
    has_bpy = "import bpy" in code
    has_dsl = "import blender_arch" in code
    if not has_bpy and not has_dsl:
        return None

    # Debe crear geometría
    creates = (
        "A.crear_" in code or "A.extruir_" in code or "A.agregar_" in code
        or "bpy.ops.mesh." in code or "bpy.data.objects.new" in code
        or ("bpy.ops.object" in code and "add" in code)
    )
    if not creates:
        return None

    tier = "mixed" if (has_bpy and has_dsl) else ("dsl" if has_dsl else "bpy")
    domain = str(it.get("domain", theme["domain"])).strip()
    if domain not in ("interior", "exterior"):
        domain = theme["domain"]

    complexity = str(it.get("complexity", "medium")).lower()
    if complexity not in ("low", "medium", "high"):
        complexity = "medium"

    return {
        "domain":      domain,
        "category":    str(it.get("category", "general")).strip(),
        "complexity":  complexity,
        "tier":        tier,
        "prompt":      prompt,
        "python_code": code,
    }


def dedup(items: list) -> list:
    seen, out = set(), []
    for it in items:
        key = re.sub(r"\s+", " ", it["prompt"].lower().strip())
        if key not in seen:
            seen.add(key)
            out.append(it)
    return out


# ---------------------------------------------------------
#  GENERACIÓN POR TEMA
# ---------------------------------------------------------

def build_prompt(count: int, theme_cfg: dict) -> str:
    has_dsl = theme_cfg["tier"] in ("dsl", "mixed")
    dsl_section = f"\n{DSL_API}\n" if has_dsl else ""
    return (
        f"Genera exactamente {count} ítems del siguiente tipo:\n\n"
        f"{theme_cfg['description']}\n"
        f"{dsl_section}"
        f"{OUTPUT_FORMAT}"
    )


def generate_theme(theme_name: str, total: int, model: str,
                   batch_size: int = 8, concurrency: int = 5) -> list:
    theme = THEMES[theme_name]
    system = (
        "Eres un arquitecto computacional experto en Blender, en el DSL blender_arch y en diseño AEC. "
        "Produces ítems de CREACIÓN para datasets de fine-tuning de modelos de lenguaje. "
        "Cada ítem tiene un prompt en español y código Python ejecutable en Blender. "
        "Prioriza la diversidad tipológica y el realismo arquitectónico."
    )

    collected = []
    rounds = 0
    max_rounds = 10

    while len(collected) < total and rounds < max_rounds:
        rounds += 1
        remaining = total - len(collected)
        n_batches = max(1, math.ceil(remaining / batch_size))
        prompts = [build_prompt(batch_size, theme) for _ in range(n_batches)]

        raw = []
        with ThreadPoolExecutor(max_workers=concurrency) as ex:
            futs = [ex.submit(call_gemini, model, system, p) for p in prompts]
            for fut in tqdm(as_completed(futs), total=len(futs),
                            desc=f"[{theme_name}] ronda {rounds}"):
                try:
                    raw.extend(fut.result())
                except Exception as e:
                    print(f"  [WARN] {e}")

        sanitized = [s for it in raw if (s := sanitize(it, theme))]
        collected.extend(sanitized)
        collected = dedup(collected)
        print(f"  → {len(collected)}/{total} válidos")

    return collected[:total]


# ---------------------------------------------------------
#  MAIN
# ---------------------------------------------------------

# Cuántos items generar por tema en modo --all
ALL_TARGETS = {
    "casas_programa":      40,
    "apartamentos":        30,
    "interiores_esp":      55,
    "espacios_colectivos": 40,
    "fachadas_modernas":   43,
    "exterior_diverso":    28,
}  # Total: 236 (regeneración de fallidos)


def main():
    ap = argparse.ArgumentParser(
        description="Genera ejemplos temáticos diversos para el dataset AEC."
    )
    ap.add_argument("--theme",      type=str, choices=list(THEMES.keys()),
                    help="Tema específico a generar.")
    ap.add_argument("--all",        action="store_true",
                    help="Genera todos los temas con sus cantidades por defecto.")
    ap.add_argument("--total",      type=int, default=None,
                    help="Número de items (solo con --theme).")
    ap.add_argument("--append-to",  type=str, default=None,
                    help="JSON existente al que acumular los nuevos items.")
    ap.add_argument("--out",        type=str, default="dataset_diverse.json",
                    help="Archivo de salida si no se usa --append-to.")
    ap.add_argument("--model",      type=str, default=DEFAULT_MODEL)
    ap.add_argument("--batch-size", type=int, default=3)
    ap.add_argument("--concurrency",type=int, default=5)
    args = ap.parse_args()

    if not os.environ.get("GOOGLE_API_KEY"):
        raise SystemExit("Falta GOOGLE_API_KEY")
    if not args.theme and not args.all:
        raise SystemExit("Usa --theme <nombre> o --all")

    # Determinar qué generar
    to_generate = {}
    if args.all:
        to_generate = ALL_TARGETS.copy()
    else:
        count = args.total or 40
        to_generate = {args.theme: count}

    print(f"\n[INFO] Plan de generación:")
    for t, n in to_generate.items():
        print(f"  {t:25s}: {n} items")
    print(f"  Total: {sum(to_generate.values())} items\n")

    # Generar
    all_new = []
    for theme_name, count in to_generate.items():
        items = generate_theme(theme_name, count, args.model,
                               args.batch_size, args.concurrency)
        print(f"[OK] {theme_name}: {len(items)} items generados\n")
        all_new.extend(items)

    # Cargar dataset existente si se pide
    existing_items: dict = {}
    if args.append_to:
        try:
            with open(args.append_to, encoding="utf-8") as f:
                existing = json.load(f)
            existing_items = existing.get("items", {})
            print(f"[INFO] Acumulando sobre {len(existing_items)} items existentes.")
        except FileNotFoundError:
            print(f"[WARN] {args.append_to} no encontrado, creando nuevo.")

    # Asignar IDs
    last_id = 0
    if existing_items:
        nums = [int(k[1:]) for k in existing_items if k.startswith("p") and k[1:].isdigit()]
        last_id = max(nums) if nums else 0

    for i, item in enumerate(all_new, start=last_id + 1):
        existing_items[f"p{i:04d}"] = item

    # Guardar
    out_file = args.append_to if args.append_to else args.out
    from collections import Counter
    tier_c = Counter(v["tier"] for v in existing_items.values())
    dom_c  = Counter(v["domain"] for v in existing_items.values())

    out_obj = {
        "meta": {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "model":      args.model,
            "language":   "es",
            "type":       "creation+code",
            "total":      len(existing_items),
            "tiers":      dict(tier_c),
            "balance":    dict(dom_c),
        },
        "items": existing_items,
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(out_obj, f, ensure_ascii=False, indent=2)

    print(f"""
[DONE] {len(all_new)} items nuevos generados.
       Total en archivo: {len(existing_items)}
       Tiers: {dict(tier_c)}
       Balance: {dict(dom_c)}
       Guardado en: {out_file}
""")


if __name__ == "__main__":
    main()
