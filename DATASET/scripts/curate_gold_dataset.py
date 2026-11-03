#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CREATION_PATH = ROOT / "DATASET" / "dataset_creation_v1.json"
EDIT_PATH = ROOT / "DATASET" / "dataset_edit_v1.json"

def fix_grammar(text):
    # Correcciones de singulares
    text = text.replace("1 estantes", "1 estante")
    text = text.replace("1 peldanos", "1 peldaño")
    text = text.replace("1 pisos", "1 piso")
    text = text.replace("1 puertas", "1 puerta")
    text = text.replace("peldanos", "peldaños")
    
    # Correcciones de género (El -> La)
    fem_nouns = ["escalera", "estanteria", "mesa", "puerta", "losa", "cama", "ventana", "silla", "columna", "fachada", "habitacion", "cocina", "piscina"]
    for noun in fem_nouns:
        text = re.sub(rf"\bal {noun}\b", f"a la {noun}", text, flags=re.IGNORECASE)
        text = re.sub(rf"\bel {noun}\b", f"la {noun}", text, flags=re.IGNORECASE)
        
    # Correcciones de "hacia izquierda"
    text = text.replace("hacia izquierda", "hacia la izquierda")
    text = text.replace("hacia derecha", "hacia la derecha")
    
    return text

def calculate_score(item):
    """Calcula un puntaje de calidad para el ejemplo (0 a 100)."""
    score = 0
    code = item.get("python_code", "")
    
    # Puntos por longitud del código
    lines = len(code.split("\n"))
    if lines > 30: score += 40
    elif lines > 15: score += 20
    elif lines > 5: score += 10
    
    # Puntos por complejidad estructural
    if "for " in code: score += 20
    if "abrir_vanos" in code: score += 15
    if "extruir" in code: score += 15
    if "_n_pisos" in code: score += 20
    if "anclar_a" in code: score += 10
    
    # Penalizar códigos excesivamente cortos (triviales)
    if lines < 5: score -= 30
    
    return max(0, min(100, score))

def main():
    print("Iniciando Curación 'Gold Standard' del Dataset...")
    
    with open(CREATION_PATH, "r", encoding="utf-8") as f:
        creation_data = json.load(f)
        
    with open(EDIT_PATH, "r", encoding="utf-8") as f:
        edit_data = json.load(f)
        
    # 1. Calificar escenas de creación
    creation_items = creation_data["items"]
    scored_creation = []
    
    for c_id, item in creation_items.items():
        score = calculate_score(item)
        scored_creation.append((score, c_id, item))
        
    # Ordenar de mejor a peor
    scored_creation.sort(key=lambda x: x[0], reverse=True)
    
    # Quedarnos con los que tengan un score mínimo (ej. mayor a 10)
    # o filtrar el 20% más bajo
    approved_creation = {c_id: item for score, c_id, item in scored_creation if score > 0}
    rejected_count = len(creation_items) - len(approved_creation)
    
    # 2. Filtrar ediciones huérfanas y corregir gramática
    edit_items = edit_data["items"]
    approved_edits = {}
    
    for e_id, item in edit_items.items():
        if item.get("base_scene_id") in approved_creation:
            # Corregir gramática del prompt
            item["instruction"] = fix_grammar(item["instruction"])
            approved_edits[e_id] = item
            
    rejected_edits = len(edit_items) - len(approved_edits)
    
    # 3. Guardar versiones actualizadas
    creation_data["items"] = approved_creation
    creation_data["meta"]["total"] = len(approved_creation)
    
    edit_data["items"] = approved_edits
    edit_data["meta"]["total"] = len(approved_edits)
    
    with open(CREATION_PATH, "w", encoding="utf-8") as f:
        json.dump(creation_data, f, ensure_ascii=False, indent=2)
        
    with open(EDIT_PATH, "w", encoding="utf-8") as f:
        json.dump(edit_data, f, ensure_ascii=False, indent=2)
        
    print(f"Curación Finalizada:")
    print(f" - Ejemplos de Creación retenidos: {len(approved_creation)} (Eliminados {rejected_count} triviales)")
    print(f" - Ejemplos de Edición retenidos: {len(approved_edits)} (Eliminados {rejected_edits} huérfanos)")
    print(" - Gramática de edición: Corregida")

if __name__ == "__main__":
    main()
