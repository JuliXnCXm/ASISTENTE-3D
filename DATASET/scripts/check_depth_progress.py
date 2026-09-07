#!/usr/bin/env python3
import json
import os
import glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT / "DATASET" / "dataset_creation_v1.json"

def main():
    if not DATASET_PATH.exists():
        print("Error: Dataset no encontrado.")
        return

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    items = data.get("items", {})
    total_items = len(items)
    
    exr_count = 0
    json_cam_count = 0
    
    # Buscar usando los paths del dataset
    for pid, item in items.items():
        blend_rel = item.get("blend_path", "")
        if blend_rel:
            dir_path = os.path.dirname(os.path.join(ROOT, "DATASET", blend_rel))
            exr_path = os.path.join(dir_path, f"{pid}_depth.exr")
            cam_path = os.path.join(dir_path, f"{pid}_camera.json")
            
            if os.path.exists(exr_path):
                exr_count += 1
            if os.path.exists(cam_path):
                json_cam_count += 1
                
    porcentaje = (exr_count / total_items) * 100
    
    print(f"=====================================")
    print(f" Progreso Generación Multimodal Depth")
    print(f"=====================================")
    print(f" Total Ítems:    {total_items}")
    print(f" Archivos EXR:   {exr_count} ({porcentaje:.2f}%)")
    print(f" Camera JSONs:   {json_cam_count}")
    print(f" Faltantes:      {total_items - exr_count}")
    print(f"=====================================")

if __name__ == "__main__":
    main()
