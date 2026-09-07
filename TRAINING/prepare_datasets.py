#!/usr/bin/env python3
"""
preparar_datasets.py
Convierte los datasets JSON canónicos de creación y edición a un formato
estándar de Hugging Face (JSONL) basado en roles (system, user, assistant).
Respeta estrictamente los splits (train, validation, test) para evitar fugas.
"""

import json
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = ROOT_DIR / "DATASET"
OUTPUT_DIR = ROOT_DIR / "TRAINING" / "data"

CREATION_JSON = DATASET_DIR / "dataset_creation_v1.json"
EDIT_JSON = DATASET_DIR / "dataset_edit_v1.json"

SYSTEM_PROMPT = """Eres un experto en desarrollo arquitectónico CAD procedural-paramétrico.
Tu tarea es generar código Python ejecutable en Blender usando el DSL 'blender_arch' y la API 'bpy'.
Escribe únicamente código Python autocontenido, sin markdown adicional ni explicaciones, a menos que se indique lo contrario."""

def ensure_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_creation_item(item_id, item):
    """Formatea un ítem de creación."""
    prompt = item.get("prompt", "")
    code = item.get("python_code", "")
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": f"```python\n{code}\n```"}
    ]
    return {"id": item_id, "task_type": "creation", "messages": messages}

def process_edit_item(item_id, item):
    """Formatea un ítem de edición (incluye el código anterior)."""
    instruction = item.get("instruction", "")
    before_code = item.get("before_python_code", "")
    after_code = item.get("after_python_code", "")
    
    user_content = f"Código actual:\n```python\n{before_code}\n```\n\nInstrucción de edición: {instruction}"
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
        {"role": "assistant", "content": f"```python\n{after_code}\n```"}
    ]
    return {"id": item_id, "task_type": "edit", "messages": messages}

def build_huggingface_jsonl():
    ensure_dirs()
    
    # Diccionarios para acumular por split
    splits = {
        "train": [],
        "validation": [],
        "test": []
    }
    
    # Procesar Creación
    if CREATION_JSON.exists():
        with open(CREATION_JSON, "r", encoding="utf-8") as f:
            data_creation = json.load(f)
            
        for item_id, item in data_creation.get("items", {}).items():
            split = item.get("split")
            if split in splits:
                splits[split].append(process_creation_item(item_id, item))
    
    # Procesar Edición
    if EDIT_JSON.exists():
        with open(EDIT_JSON, "r", encoding="utf-8") as f:
            data_edit = json.load(f)
            
        for item_id, item in data_edit.get("items", {}).items():
            split = item.get("split")
            if split in splits:
                splits[split].append(process_edit_item(item_id, item))
                
    # Escribir JSONL
    for split_name, lines in splits.items():
        out_path = OUTPUT_DIR / f"{split_name}.jsonl"
        with open(out_path, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(json.dumps(line, ensure_ascii=False) + "\n")
        print(f"Generado {split_name}.jsonl con {len(lines)} ejemplos.")

if __name__ == "__main__":
    build_huggingface_jsonl()
