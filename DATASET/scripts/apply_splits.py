#!/usr/bin/env python3
"""Aplica la asignación de splits al dataset canónico."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "dataset_creation_v1.json"
MANIFEST = ROOT / "splits" / "creation_v1_splits.json"

def main() -> None:
    dataset = json.loads(DATASET.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    
    assignments = manifest.get("assignments", {})
    if not assignments:
        raise ValueError("El manifiesto no contiene asignaciones.")
        
    items = dataset.get("items", {})
    
    for item_id, item in items.items():
        assignment = assignments.get(item_id)
        if not assignment:
            raise ValueError(f"Falta asignación para el ítem {item_id}")
            
        item["split"] = assignment["split"]
        item["family_id"] = assignment["family_id"]
        
    temporary = DATASET.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(dataset, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(DATASET)
    print(f"Dataset actualizado con éxito. {len(items)} ítems asignados a splits.")

if __name__ == "__main__":
    main()
