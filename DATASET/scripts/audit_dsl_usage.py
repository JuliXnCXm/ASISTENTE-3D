#!/usr/bin/env python3
import json
import ast
import inspect
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "DSL" / "blender"))
import blender_arch as A

DATASET_PATH = ROOT / "DATASET" / "dataset_creation_v1.json"
EDIT_PATH = ROOT / "DATASET" / "dataset_edit_v1.json"

def get_dsl_signatures():
    signatures = {}
    for name in A.__all__:
        func = getattr(A, name)
        sig = inspect.signature(func)
        signatures[name] = [p for p in sig.parameters]
    return signatures

def analyze_dataset(path, signatures):
    if not path.exists():
        return None
        
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    items = data.get("items", {})
    
    func_counts = Counter()
    missing_funcs = set(signatures.keys())
    invented_funcs = Counter()
    
    for item in items.values():
        code = item.get("python_code") or item.get("after_python_code", "")
        if not code: continue
        
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Attribute) and getattr(node.func.value, 'id', '') == 'A':
                        func_name = node.func.attr
                        
                        if func_name in signatures:
                            func_counts[func_name] += 1
                            missing_funcs.discard(func_name)
                        else:
                            invented_funcs[func_name] += 1
        except SyntaxError:
            pass
            
    return {
        "total_items": len(items),
        "func_counts": func_counts,
        "missing_funcs": missing_funcs,
        "invented_funcs": invented_funcs
    }

def main():
    signatures = get_dsl_signatures()
    print(f"Total de funciones en DSL (blender_arch.py): {len(signatures)}")
    
    print("\n--- ANALIZANDO DATASET CREACIÓN ---")
    c_res = analyze_dataset(DATASET_PATH, signatures)
    if c_res:
        print(f"Funciones usadas: {len(c_res['func_counts'])}/{len(signatures)}")
        print(f"Funciones NUNCA usadas: {len(c_res['missing_funcs'])}")
        for f in c_res['missing_funcs']:
            print(f"  - {f}")
        if c_res['invented_funcs']:
            print(f"Funciones ALUCINADAS (No existen en DSL): {len(c_res['invented_funcs'])}")
            for f, c in c_res['invented_funcs'].most_common(5):
                print(f"  - {f}: {c} veces")

    print("\n--- ANALIZANDO DATASET EDICIÓN ---")
    e_res = analyze_dataset(EDIT_PATH, signatures)
    if e_res:
        print(f"Funciones usadas: {len(e_res['func_counts'])}/{len(signatures)}")
        print(f"Funciones NUNCA usadas: {len(e_res['missing_funcs'])}")

if __name__ == "__main__":
    main()
