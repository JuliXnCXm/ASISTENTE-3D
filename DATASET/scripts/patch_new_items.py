"""
patch_new_items.py
Parchea el código de los items nuevos (p3001-p3330) con kwargs incorrectos del DSL.
"""
import json, re, os

DATASET = "dataset_v2_with_blends_with_depth.json"
NEW_START = 3001

def patch_code(code: str) -> str:
    # asignar_material: color= → base_color=
    code = re.sub(r'\basignar_material\b([^)]*?)\bcolor\s*=',
                  lambda m: m.group(0).replace('color=', 'base_color='), code)

    # crear_mesa: material= → material_tablero=
    code = re.sub(r'(crear_mesa\s*\([^)]*?)\bmaterial\s*=\s*(["\'\w\d_]+)',
                  r'\1material_tablero=\2', code)

    # crear_armario: material= → material_cuerpo=
    code = re.sub(r'(crear_armario\s*\([^)]*?)\bmaterial\s*=\s*(["\'\w\d_]+)',
                  r'\1material_cuerpo=\2', code)

    # crear_cama: material_estructura= → material_base=
    code = code.replace('material_estructura=', 'material_base=')
    # crear_cama: rotacion_z= → remove kwarg
    code = re.sub(r',\s*rotacion_z\s*=\s*[^,)\n]+(?=\s*[,)])', '', code)

    # crear_puerta: rotacion_z= → remove kwarg
    # (rotacion_z ya cubierto arriba)

    # agregar_luz: tamano= → remove kwarg
    code = re.sub(r',\s*tamano\s*=\s*[^,)\n]+(?=\s*[,)])', '', code)

    # crear_camara: rotacion= con tupla de grados → compatible (no tocar)

    return code


def main():
    with open(DATASET, encoding="utf-8") as f:
        data = json.load(f)

    items = data["items"]
    patched = 0
    skipped = 0

    for key, item in items.items():
        num = int(key[1:])
        if num < NEW_START:
            continue
        if item.get("blend_path"):
            skipped += 1
            continue

        original = item["python_code"]
        fixed = patch_code(original)
        if fixed != original:
            item["python_code"] = fixed
            patched += 1
            # Borrar .py viejo si existe para que el build lo regenere
            py_path = f"out_assets/{key}/{key}.py"
            log_path = f"out_assets/{key}/run.log"
            for p in [py_path, log_path]:
                if os.path.exists(p):
                    os.remove(p)

    with open(DATASET, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Patched: {patched} items")
    print(f"Skipped (ya tienen blend): {skipped}")
    print(f"Sin cambios: {sum(1 for k,v in items.items() if int(k[1:]) >= NEW_START and not v.get('blend_path')) - patched}")

if __name__ == "__main__":
    main()
