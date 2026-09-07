#!/usr/bin/env python3
"""
prepare_multimodal_dataset.py
Este script toma el JSONL textual generado en `prepare_datasets.py`
y lo cruza con el JSON canónico para agregar las rutas de las imágenes (RGB + Depth + Metadatos de cámara).

Esto es ideal para usar modelos como Qwen2.5-VL, LLaVA o Llava-Next.
"""

import json
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = ROOT_DIR / "DATASET"
DATA_DIR = ROOT_DIR / "TRAINING" / "data"

CREATION_JSON = DATASET_DIR / "dataset_creation_v1.json"
EDIT_JSON = DATASET_DIR / "dataset_edit_v1.json"

def get_image_info(item_id, json_data):
    """Busca en el dataset JSON la info de render."""
    if item_id in json_data.get("items", {}):
        item = json_data["items"][item_id]
        return {
            "render_path": item.get("render_path"),
            "depth_path": item.get("depth_path"),
            "metric_depth_path": item.get("metric_depth_path"),
            "camera_meta_path": item.get("camera_meta_path")
        }
    return None

def process_multimodal(split_name):
    jsonl_path = DATA_DIR / f"{split_name}.jsonl"
    out_path = DATA_DIR / f"{split_name}_multimodal.jsonl"
    
    if not jsonl_path.exists():
        print(f"Skipping {split_name} - Not found")
        return

    # Load canonical data for lookups
    with open(CREATION_JSON, "r", encoding="utf-8") as f:
        creation_data = json.load(f)
    with open(EDIT_JSON, "r", encoding="utf-8") as f:
        edit_data = json.load(f)
        
    out_lines = []
    
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            task_type = record.get("task_type")
            item_id = record.get("id")
            
            # Fetch base scene ID if it's an edit to get the original images
            base_scene_id = item_id
            if task_type == "edit" and item_id in edit_data.get("items", {}):
                base_scene_id = edit_data["items"][item_id].get("base_scene_id", item_id)
            
            img_info = get_image_info(base_scene_id, creation_data)
            
            if img_info and img_info.get("render_path"):
                # Agregamos los datos multimodales al record
                record["multimodal"] = {
                    "image": img_info["render_path"],
                    "depth_image": img_info["depth_path"],
                    "metric_depth": img_info["metric_depth_path"],
                    "camera": img_info["camera_meta_path"]
                }
                
                # Opcional: Para modelos tipo LLaVA, necesitamos añadir el token <image> al mensaje del usuario
                for msg in record["messages"]:
                    if msg["role"] == "user":
                        msg["content"] = "<image>\n" + msg["content"]
            
            out_lines.append(record)
            
    with open(out_path, "w", encoding="utf-8") as f:
        for line in out_lines:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")
            
    print(f"Generado dataset multimodal para {split_name}: {len(out_lines)} ejemplos.")

if __name__ == "__main__":
    if not DATA_DIR.exists():
        print("Corre primero prepare_datasets.py")
        sys.exit(1)
        
    process_multimodal("train")
    process_multimodal("validation")
    process_multimodal("test")
