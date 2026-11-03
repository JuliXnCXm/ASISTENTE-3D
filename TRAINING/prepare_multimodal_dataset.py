#!/usr/bin/env python3
import json
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = ROOT_DIR / "DATASET"
DATA_DIR = ROOT_DIR / "TRAINING" / "data"

CREATION_JSON = DATASET_DIR / "dataset_creation_v1.json"
EDIT_JSON = DATASET_DIR / "dataset_edit_v1.json"

def get_image_info(item_id, json_data):
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
        return

    with open(CREATION_JSON, "r", encoding="utf-8") as f:
        creation_data = json.load(f)
    with open(EDIT_JSON, "r", encoding="utf-8") as f:
        edit_data = json.load(f)
        
    out_lines = []
    
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            task_type = record.get("task_type")
            
            # ID de la escena que originó esto para poder sacar la foto
            base_scene_id = record.get("id")
            if task_type in ["edit_single", "edit_multi"]:
                # Si es un grupo multiturno o single, extraemos la base
                # buscando el ID en el dataset de edición
                if task_type == "edit_single":
                    base_scene_id = edit_data["items"][base_scene_id].get("base_scene_id")
                else: # edit_multi (el ID es seq_XXXX)
                    # Encontrar el primer item de esta secuencia
                    for e_item in edit_data["items"].values():
                        if e_item.get("multiturn_session_id") == base_scene_id:
                            base_scene_id = e_item.get("base_scene_id")
                            break
            
            img_info = get_image_info(base_scene_id, creation_data)
            
            if img_info and img_info.get("render_path"):
                record["multimodal"] = {
                    "image": img_info["render_path"],
                    "depth_image": img_info["depth_path"],
                    "metric_depth": img_info["metric_depth_path"],
                    "camera": img_info["camera_meta_path"]
                }
                
                # Para modelos LLaVA/Qwen, inyectamos <image> ÚNICAMENTE en el primer mensaje de usuario
                # (Así no enviamos la imagen repetida en cada turno del chat)
                for msg in record["messages"]:
                    if msg["role"] == "user":
                        msg["content"] = "<image>\n" + msg["content"]
                        break # Solo lo inyectamos en el primero
            
            out_lines.append(record)
            
    with open(out_path, "w", encoding="utf-8") as f:
        for line in out_lines:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    process_multimodal("train")
    process_multimodal("validation")
    process_multimodal("test")
