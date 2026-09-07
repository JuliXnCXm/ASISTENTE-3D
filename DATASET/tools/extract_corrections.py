"""
extract_corrections.py
═══════════════════════════════════════════════════════════════
CORRE ESTE SCRIPT DENTRO DE BLENDER (Text Editor → Run Script)
después de haber corregido manualmente las posiciones de los objetos.

Genera un archivo  out_assets/<pid>/<pid>_corrections.json
con las posiciones/rotaciones finales de todos los objetos de la escena.
═══════════════════════════════════════════════════════════════
"""

import bpy
import json
import math
import os

# ── Detectar el PID desde el nombre del archivo .blend abierto ──
blend_path = bpy.data.filepath
pid = os.path.splitext(os.path.basename(blend_path))[0]  # e.g. "p3002"

corrections = {}

for obj in bpy.context.scene.objects:
    if obj.type not in ('MESH', 'CURVE', 'EMPTY'):
        continue

    loc = obj.location
    rot = obj.rotation_euler   # radianes XYZ
    scl = obj.scale

    corrections[obj.name] = {
        "location":       [round(loc.x, 4), round(loc.y, 4), round(loc.z, 4)],
        "rotation_euler": [round(rot.x, 4), round(rot.y, 4), round(rot.z, 4)],
        "scale":          [round(scl.x, 4), round(scl.y, 4), round(scl.z, 4)],
    }

out_dir  = os.path.dirname(blend_path)
out_path = os.path.join(out_dir, f"{pid}_corrections.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"pid": pid, "objects": corrections}, f, indent=2, ensure_ascii=False)

print(f"[OK] Correcciones guardadas en: {out_path}")
print(f"     {len(corrections)} objetos exportados.")
print(f"\nAhora corre en terminal:")
print(f"  python tools/apply_corrections.py {pid}")
