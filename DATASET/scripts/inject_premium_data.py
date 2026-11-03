#!/usr/bin/env python3
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATASET_PATH = ROOT / "DATASET" / "dataset_creation_v1.json"

# Plantillas Maestras (Masterclass) con marcadores {VAR} para mutar matemáticamente

TPL_RASCACIELOS = """import blender_arch as A
A.limpiar_escena()

# Edificio de oficinas corporativo
edificio = A.crear_edificio_n_pisos(
    nombre="TorreCorporativa",
    pisos={PISOS},
    ancho={ANCHO}, fondo={FONDO}, alto_piso={ALTO_PISO},
    grosor_muro=0.25, grosor_losa=0.3,
    con_techo_plano=True,
    con_columnas=True, seccion_columna="rect", dim_columna=0.4,
    modulo_columna_x=4.0, modulo_columna_y=5.0,
    ventanas_fachada=True, ventana_ancho=2.0, ventana_alto=2.2,
    ventana_alfeizar=0.2, ventana_separacion=3.0,
    material_muro="{MAT_FACHADA}", material_losa="Hormigon",
    material_vidrio="Vidrio_Tintado", material_marco="Marco_Aluminio",
    material_columna="Hormigon_Visto",
    origen=(0, 0, 0)
)

# Plaza de acceso
A.crear_losa_rectangular("Plaza_Acceso", ancho={ANCHO}+10, fondo={FONDO}+10, espesor=0.15, origen=(-5, -5, -0.15), material="Concreto_Gris")

# Arbolado perimetral
for i in range(4):
    A.crear_arbol_simple(f"Arbol_Frente_{i}", radio_copa=2.0, altura_copa=4.0, altura_tronco=2.5, origen=(-3 + i*({ANCHO}+6)/3, -3, 0))
    A.crear_arbol_simple(f"Arbol_Fondo_{i}", radio_copa=2.0, altura_copa=4.0, altura_tronco=2.5, origen=(-3 + i*({ANCHO}+6)/3, {FONDO}+3, 0))
"""

TPL_VILLA = """import blender_arch as A
A.limpiar_escena()

# Casa tipo Villa con patio
casa = A.crear_casa_n_pisos(
    nombre="VillaMediterranea",
    pisos={PISOS},
    ancho={ANCHO}, fondo={FONDO}, alto_piso={ALTO_PISO},
    grosor_muro=0.2, grosor_losa=0.2,
    con_tejado=True, altura_cumbrera={CUMBRERA}, voladizo=0.6,
    material_muro="{MAT_FACHADA}", material_losa="Hormigon", material_tejado="{MAT_TEJADO}",
    origen=(0, 0, 0)
)

# Pérgola de Terraza
A.crear_columna("P_P1", ancho=0.2, fondo=0.2, alto=3.0, origen=(-2, -2, 0), material="Madera_Roble")
A.crear_columna("P_P2", ancho=0.2, fondo=0.2, alto=3.0, origen=({ANCHO}+2, -2, 0), material="Madera_Roble")
A.crear_losa_rectangular("Viga_Pergola", ancho={ANCHO}+4.4, fondo=0.4, espesor=0.2, origen=(-2.2, -2.2, 3.0), material="Madera_Roble")

# Piscina en el patio trasero
ancho_piscina = {ANCHO} * 0.6
fondo_piscina = 5.0
A.extruir_con_huecos("BordePiscina", 
    contorno=[(-1, -1), (ancho_piscina+1, -1), (ancho_piscina+1, fondo_piscina+1), (-1, fondo_piscina+1)], 
    agujeros=[[(0, 0), (ancho_piscina, 0), (ancho_piscina, fondo_piscina), (0, fondo_piscina)]], 
    altura=0.15, material="Concreto_Piso"
).location = ({ANCHO}/2 - ancho_piscina/2, {FONDO} + 2, -0.15)

A.crear_losa_rectangular("AguaPiscina", ancho=ancho_piscina, fondo=fondo_piscina, espesor=1.5, origen=({ANCHO}/2 - ancho_piscina/2, {FONDO} + 2, -1.6), material="Agua")

# Mobiliario Exterior
A.crear_mesa("MesaTerraza", ancho=2.0, fondo=1.0, alto=0.75, origen=({ANCHO}/2 - 1.0, -1.0, 0), material_tablero="Madera_Nogal", material_patas="Metal_Negro")
"""

MATERIALS = {
    "fachadas": ["Estuco", "Muro_Pintura", "Ladrillo_Rojo", "Ladrillo", "Hormigon_Visto"],
    "tejados": ["Teja", "Teja_Zinc", "Teja_Asfalt", "Cubierta_Verde"]
}

def generate_premium_dataset(num_samples=250):
    new_items = {}
    
    for i in range(num_samples):
        item_id = f"p{5000 + i:04d}"
        
        if random.random() < 0.5:
            # Rascacielos / Edificio de Oficinas
            pisos = random.randint(5, 20)
            # Rango más lógico: de 15x15m (esbelto) a 35x35m (masivo)
            ancho = round(random.uniform(15.0, 35.0), 1)
            fondo = round(random.uniform(15.0, 35.0), 1)
            alto_piso = round(random.uniform(3.0, 4.2), 1)
            mat_fachada = random.choice(MATERIALS["fachadas"])
            
            code = TPL_RASCACIELOS.replace("{PISOS}", str(pisos)).replace("{ANCHO}", str(ancho)).replace("{FONDO}", str(fondo)).replace("{ALTO_PISO}", str(alto_piso)).replace("{MAT_FACHADA}", mat_fachada)
            
            prompt = f"Construye un edificio corporativo de {pisos} pisos, de {ancho}x{fondo} metros de planta, con una fachada de {mat_fachada.replace('_', ' ').lower()} y amplios ventanales. Incluye una gran plaza perimetral de concreto con hileras de árboles bordeando el frente y el fondo del terreno."
            
            new_items[item_id] = {
                "id": item_id,
                "task_type": "creation",
                "domain": "exterior",
                "category": "edificio",
                "category_original": "edificio corporativo",
                "complexity": "high",
                "tier": "mixed",
                "prompt": prompt,
                "python_code": code,
                "blend_path": f"out_assets/{item_id}/{item_id}.blend",
                "render_path": f"out_assets/{item_id}/{item_id}_rgb.png",
                "depth_path": f"out_assets/{item_id}/{item_id}_depth.png",
                "asset_collection": f"Asset_{item_id}",
                "objects": ["TorreCorporativa", "Plaza_Acceso", "Arbol_Frente_0"],
                "units": "m",
                "coordinate_system": "RH_Z_UP",
                "split": None,
                "family_id": None,
                "validation": {
                    "syntax_status": "valid",
                    "artifact_status": "incomplete",
                    "execution_status": "not_revalidated",
                    "geometry_status": "not_evaluated",
                    "semantic_status": "not_evaluated"
                }
            }
        else:
            # Villa Residencial
            pisos = random.randint(1, 3)
            # Rango lógico: casas de 8x10m (80m2/piso) a 14x16m (220m2/piso)
            ancho = round(random.uniform(8.0, 14.0), 1)
            fondo = round(random.uniform(10.0, 16.0), 1)
            alto_piso = round(random.uniform(2.6, 3.0), 1)
            cumbrera = round(random.uniform(1.5, 2.5), 1)
            mat_fachada = random.choice(MATERIALS["fachadas"])
            mat_tejado = random.choice(MATERIALS["tejados"])
            
            code = TPL_VILLA.replace("{PISOS}", str(pisos)).replace("{ANCHO}", str(ancho)).replace("{FONDO}", str(fondo)).replace("{ALTO_PISO}", str(alto_piso)).replace("{CUMBRERA}", str(cumbrera)).replace("{MAT_FACHADA}", mat_fachada).replace("{MAT_TEJADO}", mat_tejado)
            
            prompt = f"Modela una villa residencial de {pisos} plantas con fachada de {mat_fachada.replace('_', ' ').lower()} y un tejado de {mat_tejado.replace('_', ' ').lower()}. En la parte frontal, añade una pérgola monumental de madera con columnas de 3 metros. En el patio trasero, construye una piscina con bordes de concreto de {ancho * 0.6:.1f}x5.0 metros y coloca una mesa de nogal para exteriores cerca de la pérgola."
            
            new_items[item_id] = {
                "id": item_id,
                "task_type": "creation",
                "domain": "exterior",
                "category": "casa",
                "category_original": "villa residencial",
                "complexity": "high",
                "tier": "mixed",
                "prompt": prompt,
                "python_code": code,
                "blend_path": f"out_assets/{item_id}/{item_id}.blend",
                "render_path": f"out_assets/{item_id}/{item_id}_rgb.png",
                "depth_path": f"out_assets/{item_id}/{item_id}_depth.png",
                "asset_collection": f"Asset_{item_id}",
                "objects": ["VillaMediterranea", "BordePiscina", "MesaTerraza"],
                "units": "m",
                "coordinate_system": "RH_Z_UP",
                "split": None,
                "family_id": None,
                "validation": {
                    "syntax_status": "valid",
                    "artifact_status": "incomplete",
                    "execution_status": "not_revalidated",
                    "geometry_status": "not_evaluated",
                    "semantic_status": "not_evaluated"
                }
            }

    # Leer dataset original y añadir nuevos
    if not DATASET_PATH.exists():
        print(f"Error: No se encontró el dataset en {DATASET_PATH}")
        return
        
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    dataset["items"].update(new_items)
    dataset["meta"]["total"] = len(dataset["items"])
    
    with open(DATASET_PATH, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Inyectados {num_samples} ejemplos de Nivel Maestría en {DATASET_PATH}")

if __name__ == "__main__":
    generate_premium_dataset()
