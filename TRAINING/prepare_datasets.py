#!/usr/bin/env python3
import json
import os
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = ROOT_DIR / "DATASET"
OUTPUT_DIR = ROOT_DIR / "TRAINING" / "data"

CREATION_JSON = DATASET_DIR / "dataset_creation_v1.json"
EDIT_JSON = DATASET_DIR / "dataset_edit_v1.json"

SYSTEM_PROMPT = """Eres un experto en desarrollo arquitectónico CAD procedural-paramétrico.
Tu tarea es generar código Python ejecutable en Blender usando el DSL 'blender_arch' y la API 'bpy'.
Escribe únicamente código Python autocontenido, sin markdown adicional ni explicaciones."""

def ensure_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_creation_item(item_id, item):
    prompt = item.get("prompt", "")
    code = item.get("python_code", "")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": f"{code}"}
    ]
    return {"id": item_id, "task_type": "creation", "messages": messages}

def build_huggingface_jsonl():
    ensure_dirs()
    splits = {"train": [], "validation": [], "test": []}
    
    if CREATION_JSON.exists():
        with open(CREATION_JSON, "r", encoding="utf-8") as f:
            data_creation = json.load(f)
        for item_id, item in data_creation.get("items", {}).items():
            split = item.get("split")
            if split in splits:
                splits[split].append(process_creation_item(item_id, item))
    
    if EDIT_JSON.exists():
        with open(EDIT_JSON, "r", encoding="utf-8") as f:
            data_edit = json.load(f)
            
        # Agrupar por sesiones multiturno
        sessions = defaultdict(list)
        standalone = []
        
        for item_id, item in data_edit.get("items", {}).items():
            split = item.get("split")
            if split not in splits:
                continue
            if item.get("is_multiturn"):
                sessions[item["multiturn_session_id"]].append(item)
            else:
                standalone.append(item)
                
        # Procesar ediciones independientes de 1 turno
        for item in standalone:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Código base:\n```python\n{item['before_python_code']}\n```\nInstrucción: {item['instruction']}"},
                {"role": "assistant", "content": f"{item['after_python_code']}"}
            ]
            splits[item["split"]].append({"id": item["id"], "task_type": "edit_single", "messages": messages})

        # Procesar sesiones multiturno como un Chat completo
        for session_id, turn_items in sessions.items():
            turn_items.sort(key=lambda x: x["turn_index"])
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            
            for i, turn in enumerate(turn_items):
                if i == 0:
                    messages.append({"role": "user", "content": f"Código base:\n```python\n{turn['before_python_code']}\n```\nInstrucción: {turn['instruction']}"})
                else:
                    messages.append({"role": "user", "content": turn['instruction']})
                messages.append({"role": "assistant", "content": f"{turn['after_python_code']}"})
                
            # Todos los turnos comparten el split de la escena base
            split = turn_items[0]["split"]
            splits[split].append({"id": session_id, "task_type": "edit_multi", "messages": messages})

    for split_name, lines in splits.items():
        out_path = OUTPUT_DIR / f"{split_name}.jsonl"
        with open(out_path, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(json.dumps(line, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    build_huggingface_jsonl()
