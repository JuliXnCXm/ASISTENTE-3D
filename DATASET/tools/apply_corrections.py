"""
apply_corrections.py
═══════════════════════════════════════════════════════════════
Corre en terminal después de extract_corrections.py:

    python tools/apply_corrections.py p3002

Lee  out_assets/p3002/p3002_corrections.json
y actualiza el python_code del item en el dataset:
  1. Elimina el bloque de correcciones anterior (si existe)
  2. Añade un bloque nuevo al final con las posiciones corregidas
  3. Re-renderiza depth + rgb del item corregido
═══════════════════════════════════════════════════════════════
"""

import os, sys, json, subprocess, math

DATASET   = "dataset_v2_with_blends_with_depth.json"
BLENDER   = "/snap/bin/blender"
RENDER_PY = "render_depth_test.py"

CORRECTION_HEADER = "# ── Correcciones espaciales manuales ──"
CORRECTION_FOOTER = "# ── Fin correcciones ──"

# ── Tolerancias: solo escribir si difiere del default ──
LOC_TOL = 1e-3   # metros
ROT_TOL = 1e-3   # radianes
SCL_TOL = 1e-3

DEFAULT_SCALE = [1.0, 1.0, 1.0]


def needs_correction(obj_data: dict) -> dict:
    """Devuelve solo los campos que difieren de los valores default de Blender."""
    out = {}
    loc = obj_data["location"]
    rot = obj_data["rotation_euler"]
    scl = obj_data["scale"]

    if any(abs(v) > LOC_TOL for v in loc):
        out["location"] = loc
    if any(abs(v) > ROT_TOL for v in rot):
        out["rotation_euler"] = rot
    if any(abs(scl[i] - DEFAULT_SCALE[i]) > SCL_TOL for i in range(3)):
        out["scale"] = scl
    return out


def build_correction_block(objects: dict) -> str:
    lines = [CORRECTION_HEADER]
    lines.append("import bpy as _bpy")
    lines.append("_objs = _bpy.data.objects")

    for name, data in sorted(objects.items()):
        corr = needs_correction(data)
        if not corr:
            continue
        safe = name.replace("'", "\\'")
        if "location" in corr:
            x, y, z = corr["location"]
            lines.append(f"if '{safe}' in _objs: _objs['{safe}'].location = ({x}, {y}, {z})")
        if "rotation_euler" in corr:
            rx, ry, rz = corr["rotation_euler"]
            lines.append(
                f"if '{safe}' in _objs: _objs['{safe}'].rotation_euler = ({rx}, {ry}, {rz})"
            )
        if "scale" in corr:
            sx, sy, sz = corr["scale"]
            lines.append(f"if '{safe}' in _objs: _objs['{safe}'].scale = ({sx}, {sy}, {sz})")

    lines.append(CORRECTION_FOOTER)
    return "\n".join(lines)


def strip_old_corrections(code: str) -> str:
    """Elimina un bloque de correcciones previo si existe."""
    if CORRECTION_HEADER not in code:
        return code
    start = code.index(CORRECTION_HEADER)
    end   = code.find(CORRECTION_FOOTER, start)
    if end == -1:
        return code[:start].rstrip()
    return code[:start].rstrip() + "\n" + code[end + len(CORRECTION_FOOTER):].lstrip()


def main():
    if len(sys.argv) < 2:
        print("Uso: python tools/apply_corrections.py <pid>")
        sys.exit(1)

    pid = sys.argv[1]

    # ── Cargar correcciones ──
    corr_path = os.path.join("out_assets", pid, f"{pid}_corrections.json")
    if not os.path.exists(corr_path):
        print(f"[ERROR] No se encontró: {corr_path}")
        print("        Corre primero extract_corrections.py dentro de Blender.")
        sys.exit(1)

    with open(corr_path, encoding="utf-8") as f:
        corr_data = json.load(f)

    objects = corr_data["objects"]
    print(f"[INFO] {len(objects)} objetos en correcciones")

    # ── Cargar dataset ──
    with open(DATASET, encoding="utf-8") as f:
        dataset = json.load(f)

    if pid not in dataset["items"]:
        print(f"[ERROR] {pid} no encontrado en el dataset.")
        sys.exit(1)

    item = dataset["items"][pid]
    original_code = item["python_code"]

    # ── Construir y aplicar bloque de correcciones ──
    clean_code       = strip_old_corrections(original_code)
    correction_block = build_correction_block(objects)

    if correction_block.count("\n") <= 3:
        print("[INFO] No hay diferencias significativas respecto a defaults. Nada que corregir.")
        return

    new_code = clean_code.rstrip() + "\n\n" + correction_block
    item["python_code"] = new_code

    # ── Guardar dataset ──
    with open(DATASET, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    print(f"[OK] python_code de {pid} actualizado en {DATASET}")

    # ── Re-build el .blend con el código corregido ──
    blend_path = os.path.join("out_assets", pid, f"{pid}.blend")
    print(f"[INFO] Re-buildeando {blend_path}...")
    result = subprocess.run([
        BLENDER, "-b", "-P", "build_blends_from_dataset.py", "--",
        "--dataset", DATASET,
        "--out", "out_assets",
        "--update-json-out", DATASET,
        "--ids", pid,
    ], capture_output=True, text=True)

    if "FAIL: 1" in result.stdout:
        print(f"[WARN] Re-build falló. Revisa el código generado.")
        print(result.stdout[-500:])
    else:
        print(f"[OK] .blend re-buildeado.")

    # ── Re-renderizar depth + rgb ──
    print(f"[INFO] Re-renderizando depth + rgb...")
    # Eliminar renders anteriores para forzar re-render
    for suffix in ["_rgb.png", "_depth.png"]:
        p = os.path.join("out_assets", pid, f"{pid}{suffix}")
        if os.path.exists(p):
            os.remove(p)

    result2 = subprocess.run([
        BLENDER, "-b", "-P", RENDER_PY, "--",
        "--dataset", DATASET,
        "--out", "out_assets",
        "--ids", pid,
    ], capture_output=True, text=True)

    if "[OK]" in result2.stdout:
        print(f"[OK] Renders actualizados.")
    else:
        print(f"[WARN] Render con problemas.")
        print(result2.stdout[-300:])

    print(f"\n[DONE] {pid} corregido completamente.")


if __name__ == "__main__":
    main()
