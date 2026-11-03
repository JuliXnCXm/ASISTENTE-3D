#!/usr/bin/env python3
"""
generate_edit_dataset.py
Motor avanzado de mutación AST para crear secuencias de edición paramétricas.
Genera cambios en dimensiones, posición, adición, eliminación y parámetros estructurales,
con control de validez lógica y secuencias multiturno.
"""

import json
import ast
import random
import copy
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent.parent
DATASET_PATH = ROOT / "DATASET" / "dataset_creation_v1.json"
OUTPUT_PATH = ROOT / "DATASET" / "dataset_edit_v1.json"

SEMANTIC_DIRECTIONS = [
    "hacia la izquierda", "a la derecha", "hacia adelante", "hacia el fondo"
]

GRAMMAR_MAP = {
    "silla": "una silla",
    "mesa": "una mesa",
    "columna": "una columna",
    "arbol_simple": "un árbol",
    "ventana": "una ventana",
    "puerta": "una puerta",
    "muro": "un muro",
    "losa_rectangular": "una losa",
    "sofa": "un sofá",
    "estanteria": "una estantería"
}

def get_ast_call_name(call_node):
    """Extrae el nombre de la función invocada."""
    if isinstance(call_node.func, ast.Attribute) and getattr(call_node.func.value, 'id', '') == 'A':
        return call_node.func.attr
    return None

class ASTMutator(ast.NodeTransformer):
    def __init__(self):
        self.mutations = []
        self.mutated = False

    def visit_Module(self, node):
        if self.mutated:
            return node

        # Recopilar llamadas a la DSL
        valid_calls = []
        for i, stmt in enumerate(node.body):
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                func_name = get_ast_call_name(stmt.value)
                if func_name and func_name.startswith("crear_"):
                    valid_calls.append((i, func_name, stmt))

        # Determinar aleatoriamente qué tipo de mutación hacer en TODO el script
        # 0: Eliminación múltiple
        # 1: Eliminación simple
        # 2: Adición
        # 3: Dejar pasar a visit_Call para mutar argumentos internos (dimensión, material, etc)
        
        mutation_choice = random.choices([0, 1, 2, 3], weights=[0.05, 0.10, 0.15, 0.70])[0]

        if mutation_choice == 0 and valid_calls and len(valid_calls) > 2:
            counts = defaultdict(list)
            for idx, fname, _ in valid_calls:
                counts[fname].append(idx)
            
            multiples = {k: v for k, v in counts.items() if len(v) >= 2}
            if multiples:
                target_func = random.choice(list(multiples.keys()))
                indices = multiples[target_func]
                
                for idx in sorted(indices, reverse=True):
                    node.body.pop(idx)
                
                name_clean = target_func.replace("crear_", "").replace("_", " ")
                self.mutated = True
                self.mutations.append({
                    "type": "multi_deletion",
                    "prompt": random.choice([
                        f"Elimina todas las ocurrencias de {name_clean}.",
                        f"Borra todos los elementos de tipo {name_clean} de la escena."
                    ])
                })
                return node

        elif mutation_choice == 1 and valid_calls and len(valid_calls) > 1:
            idx, func_name, _ = random.choice(valid_calls)
            node.body.pop(idx)
            self.mutated = True
            name_clean = func_name.replace("crear_", "").replace("_", " ")
            self.mutations.append({
                "type": "deletion",
                "prompt": f"Quita el elemento {name_clean} que está en la escena."
            })
            return node

        elif mutation_choice == 2:
            new_obj = random.choice(list(GRAMMAR_MAP.keys()))
            x, y = round(random.uniform(-3, 3), 1), round(random.uniform(-3, 3), 1)
            new_code = f"A.crear_{new_obj}('{new_obj.capitalize()}_Nuevo', origen=({x}, {y}, 0.0))"
            new_stmt = ast.parse(new_code).body[0]
            node.body.append(new_stmt)
            self.mutated = True
            self.mutations.append({
                "type": "addition",
                "prompt": f"Añade {GRAMMAR_MAP[new_obj]} en las coordenadas X={x}, Y={y}."
            })
            return node

        # Si llegamos aquí (mutation_choice == 3 o fallaron los anteriores), vamos a mutar parámetros
        self.generic_visit(node)
        return node

    def visit_Call(self, node):
        if self.mutated:
            return node
            
        func_name = get_ast_call_name(node)
        if not func_name:
            self.generic_visit(node)
            return node

        # Barajar los keywords para que la mutación sea aleatoria
        # (A veces cambiará el material, a veces la posición, a veces la dimensión)
        kws = list(node.keywords)
        random.shuffle(kws)

        for kw in kws:
            # 4. CAMBIO ESTRUCTURAL
            if kw.arg in ['pisos', 'num_pisos', 'num_estantes', 'num_peldanos', 'num_puertas'] and isinstance(kw.value, ast.Constant):
                if isinstance(kw.value.value, int):
                    old_val = kw.value.value
                    if 'edificio' in func_name.lower() or 'casa' in func_name.lower():
                        delta = random.choice([2, 3, 5, -2, -3])
                    else:
                        delta = random.choice([1, 2, -1, -2])
                        
                    new_val = max(1, old_val + delta)
                    if new_val != old_val:
                        kw.value = ast.Constant(value=new_val)
                        if 'edificio' in func_name.lower() or 'casa' in func_name.lower():
                            noun = "niveles" if random.random() > 0.5 else "pisos"
                            target_name = "la torre" if 'edificio' in func_name.lower() else "la villa"
                        else:
                            noun = kw.arg.replace('num_', '').replace('pisos', 'piso(s)')
                            target_name = func_name.replace('crear_', '').replace('_', ' ')
                            
                        action = "Agrégale" if delta > 0 else "Quítale"
                        prompt = f"{action} {abs(delta)} {noun} a {target_name}."
                        self.mutated = True
                        self.mutations.append({"type": "structural_change", "prompt": prompt})
                        return node

            # 5. CAMBIO DIMENSIONAL
            elif kw.arg in ['ancho', 'alto', 'largo', 'fondo', 'radio', 'ancho_piscina', 'fondo_piscina'] and isinstance(kw.value, ast.Constant):
                if isinstance(kw.value.value, (int, float)) and kw.value.value > 0.1:
                    old_val = kw.value.value
                    if old_val > 10.0:
                        factor = random.choice([1.2, 1.4, 0.8, 0.6])
                    else:
                        factor = random.choice([1.3, 1.5, 0.7, 0.5])
                        
                    new_val = round(old_val * factor, 2)
                    kw.value = ast.Constant(value=new_val)
                    action = "Extiende" if factor > 1 else "Acorta"
                    param_name = kw.arg.replace('_piscina', '')
                    obj_name = func_name.replace('crear_','').replace('extruir_con_huecos','la geometría base')
                    if 'edificio' in func_name.lower(): obj_name = "el rascacielos"
                    elif 'casa' in func_name.lower(): obj_name = "la casa"
                    
                    self.mutated = True
                    self.mutations.append({
                        "type": "dimension_change",
                        "prompt": f"{action} el parámetro '{param_name}' de {obj_name} para que sea de {new_val} metros."
                    })
                    return node

            # 6. ROTACIÓN
            elif kw.arg == 'rotacion_z' and isinstance(kw.value, ast.Constant):
                if isinstance(kw.value.value, (int, float)):
                    old_rot = kw.value.value
                    delta_rot = random.choice([90, -90, 45, -45, 180])
                    new_rot = (old_rot + delta_rot) % 360
                    kw.value = ast.Constant(value=new_rot)
                    self.mutated = True
                    self.mutations.append({
                        "type": "rotation_change",
                        "prompt": f"Aplica una rotación adicional de {delta_rot} grados en el eje Z al objeto."
                    })
                    return node

            # 7. POSICIONAMIENTO
            elif kw.arg == 'origen' and isinstance(kw.value, ast.Tuple) and len(kw.value.elts) == 3:
                if all(isinstance(e, ast.Constant) for e in kw.value.elts):
                    old_x, old_y, old_z = [e.value for e in kw.value.elts]
                    axis = random.choice([0, 1])
                    delta = round(random.uniform(0.5, 3.0) * random.choice([1, -1]), 2)
                    
                    if axis == 0:
                        kw.value.elts[0] = ast.Constant(value=round(old_x + delta, 2))
                        dir_str = "derecha" if delta > 0 else "izquierda"
                    else:
                        kw.value.elts[1] = ast.Constant(value=round(old_y + delta, 2))
                        dir_str = "el fondo" if delta > 0 else "el frente"
                        
                    prompt = random.choice([
                        f"Desplaza el objeto {abs(delta)} metros hacia {dir_str}.",
                        f"Mueve el objeto {abs(delta)} metros en el eje {'X' if axis==0 else 'Y'}."
                    ])
                    
                    self.mutated = True
                    self.mutations.append({
                        "type": "position_change",
                        "prompt": prompt
                    })
                    return node

        self.generic_visit(node)
        return node


def apply_mutation(code_str: str):
    """Aplica una única mutación al código AST y devuelve (nuevo_codigo, meta)."""
    try:
        tree = ast.parse(code_str)
    except SyntaxError:
        return None, None
        
    mutator = ASTMutator()
    new_tree = mutator.visit(copy.deepcopy(tree))
    
    if not mutator.mutated:
        return None, None
        
    ast.fix_missing_locations(new_tree)
    new_code = ast.unparse(new_tree)
    return new_code, mutator.mutations[0]


def build_multiturn_chain(base_code: str, num_turns: int):
    """Encadena mutaciones para simular un chat de N turnos."""
    turns = []
    current_code = base_code
    for _ in range(num_turns):
        new_code, meta = apply_mutation(current_code)
        if not new_code:
            break
        turns.append({
            "instruction": meta["prompt"],
            "before_code": current_code,
            "after_code": new_code,
            "edit_type": meta["type"]
        })
        current_code = new_code
    return turns


def main():
    if not DATASET_PATH.exists():
        print(f"Error: No se encontró {DATASET_PATH}")
        return

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    items = dataset.get("items", {})
    edit_items = {}
    edit_idx = 1

    print("Generando dataset de edición (AST Mutations)...")

    for base_id, item in items.items():
        if item.get("tier") not in ["dsl", "mixed"]:
            continue
            
        base_code = item["python_code"]
        split = item.get("split")
        family = item.get("family_id")
        
        # 1. Single Turn Edition
        new_code, meta = apply_mutation(base_code)
        if new_code:
            e_id = f"e{edit_idx:04d}"
            edit_items[e_id] = {
                "id": e_id,
                "task_type": "edit",
                "base_scene_id": base_id,
                "domain": item["domain"],
                "category": item["category"],
                "split": split,
                "family_id": family,
                "edit_type": meta["type"],
                "instruction": meta["prompt"],
                "before_python_code": base_code,
                "after_python_code": new_code,
                "turn_index": 1,
                "is_multiturn": False
            }
            edit_idx += 1

        # 2. Multi Turn Edition (20% probability)
        if random.random() < 0.20:
            chain = build_multiturn_chain(base_code, num_turns=random.randint(2, 4))
            if len(chain) > 1:
                session_id = f"seq_{edit_idx:04d}"
                for i, step in enumerate(chain):
                    e_id = f"e{edit_idx:04d}"
                    edit_items[e_id] = {
                        "id": e_id,
                        "task_type": "edit",
                        "base_scene_id": base_id,
                        "domain": item["domain"],
                        "category": item["category"],
                        "split": split,
                        "family_id": family,
                        "edit_type": step["edit_type"],
                        "instruction": step["instruction"],
                        "before_python_code": step["before_code"],
                        "after_python_code": step["after_code"],
                        "turn_index": i + 1,
                        "is_multiturn": True,
                        "multiturn_session_id": session_id
                    }
                    edit_idx += 1

    out_payload = {
        "meta": {
            "schema_version": "1.0.0",
            "dataset_version": "edit-v4.0.0",
            "task_type": "edit",
            "total": len(edit_items),
            "source_dataset": DATASET_PATH.name
        },
        "items": edit_items
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out_payload, f, ensure_ascii=False, indent=2)

    print(f"Dataset guardado en {OUTPUT_PATH}")
    print(f"Total ejemplos generados: {len(edit_items)}")

if __name__ == "__main__":
    main()

# Añado una regla de eliminación de bloques for (Ej: "Quita todos los árboles perimetrales")
def remove_for_loops(node):
    for i, stmt in enumerate(node.body):
        if isinstance(stmt, ast.For):
            # Buscar si el loop crea algo con 'A.crear_'
            for inner in stmt.body:
                if isinstance(inner, ast.Expr) and isinstance(inner.value, ast.Call):
                    func_name = get_ast_call_name(inner.value)
                    if func_name and "crear_" in func_name:
                        obj_type = func_name.replace("crear_", "")
                        node.body.pop(i)
                        return True, f"Elimina todas las ocurrencias de {obj_type.replace('_', ' ')} que estén en grupo/formación."
    return False, ""

# Modificar visit_Module para integrarlo
original_visit_Module = ASTMutator.visit_Module
def new_visit_Module(self, node):
    if not self.mutated:
        rand_val = random.random()
        # 5% Probabilidad: Eliminar un bucle for entero (ej. árboles perimetrales o columnas)
        if rand_val < 0.05:
            success, prompt = remove_for_loops(node)
            if success:
                self.mutated = True
                self.mutations.append({
                    "type": "block_deletion",
                    "prompt": prompt
                })
                return node
    return original_visit_Module(self, node)

ASTMutator.visit_Module = new_visit_Module
