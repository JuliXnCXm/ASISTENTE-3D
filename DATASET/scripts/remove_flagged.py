# remove_flagged.py
# Lee un flagged_ids.json exportado desde la galería y elimina
# esos items del dataset JSON.
#
# Uso:
#   python remove_flagged.py --dataset dataset_v2_with_renders.json \
#                            --flagged flagged_ids.json
#
# Opcional:
#   --out dataset_v2_curated.json   (por defecto sobreescribe el dataset)
#   --dry-run                       (muestra qué se eliminaría sin modificar)

import json
import os
import argparse
from datetime import datetime, timezone


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, help="JSON del dataset a curar")
    ap.add_argument("--flagged", required=True, help="flagged_ids.json exportado desde la galería")
    ap.add_argument("--out", default=None, help="Ruta de salida (si no, sobreescribe --dataset)")
    ap.add_argument("--dry-run", action="store_true", help="Solo muestra qué se eliminaría")
    return ap.parse_args()


def main():
    args = parse_args()

    with open(args.dataset, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items", {})

    with open(args.flagged, "r", encoding="utf-8") as f:
        flagged_data = json.load(f)
    flagged_ids = set(flagged_data.get("flagged_ids", []))

    not_found = flagged_ids - set(items.keys())
    to_remove = flagged_ids & set(items.keys())

    print(f"Items en dataset:      {len(items)}")
    print(f"IDs marcados:          {len(flagged_ids)}")
    print(f"IDs no encontrados:    {len(not_found)}")
    print(f"A eliminar:            {len(to_remove)}")

    if not_found:
        print(f"  [WARN] No encontrados: {sorted(not_found)}")

    if args.dry_run:
        print("\n[DRY-RUN] No se realizaron cambios.")
        print("IDs que se eliminarían:")
        for pid in sorted(to_remove):
            print(f"  {pid}  |  {items[pid].get('tier','?')}  |  {items[pid].get('prompt','')[:80]}")
        return

    for pid in to_remove:
        del items[pid]

    data["meta"]["total"] = len(items)
    data["meta"]["updated_at"] = datetime.now(timezone.utc).isoformat()

    out_path = args.out or args.dataset
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Dataset actualizado: {out_path}")
    print(f"     Total final: {len(items)} items")


if __name__ == "__main__":
    main()
