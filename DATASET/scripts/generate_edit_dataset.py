#!/usr/bin/env python3
"""
Motor de mutación AST para generar el Dataset de Edición.
Toma escenas de creación válidas y aplica mutaciones programáticas
para generar pares `antes -> instrucción -> después`.
"""

import json
import ast
import random
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT / "dataset_creation_v1.json"
OUTPUT_PATH = ROOT / "dataset_edit_v1.json"

# Materiales mapeados por categoría para mutaciones lógicas
MATERIAL_SWAPS = {
    "muro": ["Ladrillo_Rojo", "Muro_Pintura", "Muro_Pintura_Gris", "Estuco", "Yeso", "Hormigon_Visto"],
    "piso": ["Parquet", "Ceramica_Piso", "Porcelanato", "Concreto_Piso", "Piso_Madera", "Alfombra"],
    "madera": ["Madera_Roble", "Madera_Nogal", "Madera_Wengue", "MDF_Blanco", "Melanina_Gris"],
    "metal": ["Acero", "Acero_Inox", "Aluminio", "Cobre", "Bronce", "Metal_Negro"],
    "tela": ["Tela_Gris", "Tela_Beige", "Tela_Azul", "Cuero", "Cuero_Negro"]
}

class ASTMutator(ast.NodeTransformer):
    def __init__(self, target_func_names=None):
        self.target_func_names = target_func_names or []
        self.mutations_applied = []
        self.mutated = False

    def visit_Module(self, node):
        if not self.mutated:
            calls = []
            for i, stmt in enumerate(node.body):
                if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                    if isinstance(stmt.value.func, ast.Attribute) and isinstance(stmt.value.func.value, ast.Name) and stmt.value.func.value.id == 'A':
                        calls.append((i, stmt.value.func.attr))

            rand_val = random.random()
            if calls and len(calls) > 1 and rand_val < 0.15: # 15% borrar
                idx_to_remove, func_name = random.choice(calls)
                node.body.pop(idx_to_remove)
                self.mutated = True
                obj_type = func_name.replace("crear_", "").replace("_", " ")
                self.mutations_applied.append({
                    "type": "deletion",
                    "target": func_name,
                    "prompt": f"Elimina {obj_type} de la escena."
                })
                return node
                
            elif rand_val < 0.30: # 15% añadir
                new_obj = random.choice(["silla", "mesa", "columna", "arbol_simple"])
                new_stmt = ast.parse(f"A.crear_{new_obj}('{new_obj.capitalize()}_Nuevo', origen=({round(random.uniform(-2, 2), 1)}, {round(random.uniform(-2, 2), 1)}, 0))").body[0]
                node.body.append(new_stmt)
                self.mutated = True
                self.mutations_applied.append({
                    "type": "addition",
                    "target": f"crear_{new_obj}",
                    "prompt": f"Añade un {new_obj.replace('_', ' ')} a la escena."
                })
                return node
                
        # Si no hizo eliminación o adición, delega a visit_Call para cambiar dimensiones/materiales
        self.generic_visit(node)
        return node

    def visit_Call(self, node):
        self.generic_visit(node)
        
        # Verificar si es una llamada a la API DSL (ej. A.crear_muro)
        is_target_func = False
        func_name = ""
        
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == 'A':
                func_name = node.func.attr
                if not self.target_func_names or func_name in self.target_func_names:
                    is_target_func = True
        elif isinstance(node.func, ast.Name):
            func_name = node.func.id
            if not self.target_func_names or func_name in self.target_func_names:
                is_target_func = True

        if is_target_func and not self.mutated:
            # Intentar mutar material
            for kw in node.keywords:
                if kw.arg and 'material' in kw.arg and isinstance(kw.value, ast.Constant):
                    old_mat = kw.value.value
                    
                    # Encontrar una categoría compatible
                    for cat, mats in MATERIAL_SWAPS.items():
                        if old_mat in mats or any(m.lower() in str(old_mat).lower() for m in mats):
                            new_mats = [m for m in mats if m != old_mat]
                            if new_mats:
                                new_mat = random.choice(new_mats)
                                kw.value = ast.Constant(value=new_mat)
                                self.mutated = True
                                self.mutations_applied.append({
                                    "type": "material_change",
                                    "target": func_name,
                                    "old": old_mat,
                                    "new": new_mat,
                                    "prompt": f"Cambia el material a {new_mat.replace('_', ' ').lower()}."
                                })
                                return node
            
            # Intentar mutar dimensión (si no mutó material)
            for kw in node.keywords:
                if kw.arg in ['ancho', 'alto', 'largo', 'fondo'] and isinstance(kw.value, ast.Constant):
                    if isinstance(kw.value.value, (int, float)):
                        old_dim = kw.value.value
                        # Cambiar dimensión en un 20%
                        factor = random.choice([1.2, 0.8])
                        new_dim = round(old_dim * factor, 2)
                        
                        action = "Aumenta" if factor > 1 else "Reduce"
                        
                        kw.value = ast.Constant(value=new_dim)
                        self.mutated = True
                        self.mutations_applied.append({
                            "type": "dimension_change",
                            "target": func_name,
                            "param": kw.arg,
                            "old": old_dim,
                            "new": new_dim,
                            "prompt": f"{action} el {kw.arg} a {new_dim} metros."
                        })
                        return node

            # Intentar mutar rotación
            for kw in node.keywords:
                if kw.arg == 'rotacion_z' and isinstance(kw.value, ast.Constant):
                    if isinstance(kw.value.value, (int, float)):
                        old_rot = kw.value.value
                        # Rotar 90, -90 o 180 grados adicionales
                        delta_rot = random.choice([90, -90, 180])
                        new_rot = (old_rot + delta_rot) % 360
                        
                        kw.value = ast.Constant(value=new_rot)
                        self.mutated = True
                        self.mutations_applied.append({
                            "type": "rotation_change",
                            "target": func_name,
                            "param": "rotacion_z",
                            "old": old_rot,
                            "new": new_rot,
                            "prompt": f"Gira el objeto {abs(delta_rot)} grados."
                        })
                        return node
            # Intentar mutar origen/posición (si no mutó dimensión, material ni rotación)
            for kw in node.keywords:
                if kw.arg == 'origen' and isinstance(kw.value, ast.Tuple):
                    # El origen es una tupla (x, y, z)
                    if len(kw.value.elts) == 3 and all(isinstance(e, ast.Constant) for e in kw.value.elts):
                        old_x = kw.value.elts[0].value
                        old_y = kw.value.elts[1].value
                        old_z = kw.value.elts[2].value
                        
                        # Elegir un eje para mover (0=X, 1=Y) - Evitamos mover en Z para no enterrar/volar objetos
                        axis = random.choice([0, 1])
                        axis_name = "X" if axis == 0 else "Y"
                        
                        # Desplazamiento aleatorio entre -2.0 y 2.0 metros
                        desplazamiento = round(random.uniform(0.5, 2.0) * random.choice([1, -1]), 2)
                        
                        new_x = old_x + desplazamiento if axis == 0 else old_x
                        new_y = old_y + desplazamiento if axis == 1 else old_y
                        new_z = old_z
                        
                        # Actualizar el AST
                        kw.value.elts[0] = ast.Constant(value=new_x)
                        kw.value.elts[1] = ast.Constant(value=new_y)
                        
                        dir_name = "la derecha" if desplazamiento > 0 and axis == 0 else "la izquierda" if desplazamiento < 0 and axis == 0 else "el fondo" if desplazamiento > 0 and axis == 1 else "el frente"
                        
                        self.mutated = True
                        self.mutations_applied.append({
                            "type": "position_change",
                            "target": func_name,
                            "param": "origen",
                            "old": (old_x, old_y, old_z),
                            "new": (new_x, new_y, new_z),
                            "prompt": f"Mueve el objeto {abs(desplazamiento)} metros hacia {dir_name} (eje {axis_name})."
                        })
                        return node

        return node

def mutate_code(original_code: str):
    """
    Toma un código Python y aplica una mutación AST válida.
    Devuelve el código nuevo y la metadata de la mutación.
    """
    try:
        tree = ast.parse(original_code)
    except SyntaxError:
        return None, []
        
    mutator = ASTMutator()
    new_tree = mutator.visit(copy.deepcopy(tree))
    
    if not mutator.mutated:
        return None, []
        
    ast.fix_missing_locations(new_tree)
    new_code = ast.unparse(new_tree)
    
    return new_code, mutator.mutations_applied

def main():
    if not DATASET_PATH.exists():
        print(f"Error: No se encontró {DATASET_PATH}")
        return
        
    print("Cargando dataset canónico...")
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)
        
    items = dataset.get("items", {})
    edit_items = {}
    
    print("Generando mutaciones de edición...")
    edit_id_counter = 1
    
    for item_id, item in items.items():
        if item.get("tier") not in ["dsl", "mixed"]:
            continue # Solo mutamos las que usan la DSL estructurada
            
        original_code = item["python_code"]
        new_code, mutations = mutate_code(original_code)
        
        if new_code and mutations:
            mutation = mutations[0]
            edit_id = f"e{edit_id_counter:04d}"
            
            edit_items[edit_id] = {
                "id": edit_id,
                "task_type": "edit",
                "base_scene_id": item_id,
                "domain": item["domain"],
                "category": item["category"],
                "split": item["split"], # IMPORTANTE: Hereda el split para evitar fuga
                "family_id": item.get("family_id"),
                "edit_type": mutation["type"],
                "instruction": mutation["prompt"],
                "before_python_code": original_code,
                "after_python_code": new_code,
                "target_function": mutation["target"],
                "changed_parameter": mutation.get("param", "objeto"),
                "old_value": mutation.get("old", ""),
                "new_value": mutation.get("new", "")
            }
            edit_id_counter += 1
            
            # Generar solo una mutación por escena base por ahora
            # para no desbalancear el dataset.

    edit_dataset = {
        "meta": {
            "schema_version": "1.0.0",
            "dataset_version": "edit-v1.0.0",
            "task_type": "edit",
            "total": len(edit_items),
            "generated_at": dataset["meta"]["generated_at"],
            "source_dataset": DATASET_PATH.name
        },
        "items": edit_items
    }
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(edit_dataset, f, ensure_ascii=False, indent=2)
        
    print(f"Generado dataset de edición con {len(edit_items)} ejemplos.")
    print(f"Guardado en: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
