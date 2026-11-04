#!/usr/bin/env python3
"""
auditar_multimodal.py
Audita TODAS las referencias multimodales de TRAINING/data/*_multimodal.jsonl:
  - existencia local (DATASET/<ruta>) y en Hugging Face (julianG99/aec-procedural-blender)
  - PNG RGB: legible, tamaño, ¿imagen vacía? (desviación estándar ~0)
  - EXR métrico: legible, % de píxeles infinitos/fondo, rango de profundidad
  - camera.json: claves, ¿extrínseca identidad? (cámara sin colocar)
Uso:
  python DATASET/tools/auditar_multimodal.py [--sin_hf] [--max N]
Salida: DATASET/reports/auditoria_multimodal.json + resumen en consola.
"""
import os, sys, json, argparse, collections
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import numpy as np
import cv2
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))           # ASISTENTE-3D
DATASET = os.path.join(ROOT, "DATASET")
DATA = os.path.join(ROOT, "TRAINING", "data")
HF_REPO = "julianG99/aec-procedural-blender"


def leer_jsonl_tolerante(path):
    s = open(path, encoding="utf-8").read()
    dec, i, rows = json.JSONDecoder(), 0, []
    while i < len(s):
        while i < len(s) and s[i] in " \n\t\r,[]":
            i += 1
        if i >= len(s):
            break
        o, i = dec.raw_decode(s, i)
        rows.append(o)
    return rows


def es_identidad(m):
    try:
        return np.allclose(np.array(m, dtype=float), np.eye(4), atol=1e-6)
    except Exception:
        return False


def auditar_asset(scene_id, mm):
    r = {"scene": scene_id, "problemas": []}
    # RGB
    p = os.path.join(DATASET, mm.get("image") or "")
    if not mm.get("image") or not os.path.isfile(p):
        r["problemas"].append("rgb_falta")
    else:
        try:
            im = np.asarray(Image.open(p).convert("RGB"), dtype=np.float32)
            r["rgb_size"] = list(im.shape[:2])
            r["rgb_std"] = float(im.std())
            if im.std() < 1.0:
                r["problemas"].append("rgb_vacia")
        except Exception as e:
            r["problemas"].append(f"rgb_ilegible:{e}")
    # EXR
    p = os.path.join(DATASET, mm.get("metric_depth") or "")
    if not mm.get("metric_depth") or not os.path.isfile(p):
        r["problemas"].append("exr_falta")
    else:
        d = cv2.imread(p, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        if d is None:
            r["problemas"].append("exr_ilegible")
        else:
            if d.ndim == 3 and not (np.allclose(d[..., 0], d[..., 1]) and np.allclose(d[..., 1], d[..., 2])):
                r["problemas"].append("exr_no_es_profundidad")
            d = d[..., 0] if d.ndim == 3 else d
            fin = np.isfinite(d) & (d < 1e4) & (d > 0)
            r["exr_pct_fondo"] = round(float(1 - fin.mean()) * 100, 1)
            if fin.any():
                r["exr_min"], r["exr_max"] = float(d[fin].min()), float(d[fin].max())
            if fin.mean() < 0.02:
                r["problemas"].append("exr_sin_geometria")
            r["exr_tiene_fondo"] = bool((~np.isfinite(d)).any() or (d >= 1e4).any())
    # Cámara
    p = os.path.join(DATASET, mm.get("camera") or "")
    if not mm.get("camera") or not os.path.isfile(p):
        r["problemas"].append("cam_falta")
    else:
        try:
            c = json.load(open(p))
            r["cam_claves"] = sorted(c.keys())
            if es_identidad(c.get("cam_to_world")):
                r["problemas"].append("cam_identidad")
            if c.get("generator_version") is None:
                r["problemas"].append("cam_version_vieja")
        except Exception as e:
            r["problemas"].append(f"cam_ilegible:{e}")
    # depth png (visual)
    p = os.path.join(DATASET, mm.get("depth_image") or "")
    if mm.get("depth_image") and not os.path.isfile(p):
        r["problemas"].append("depthpng_falta")
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sin_hf", action="store_true")
    ap.add_argument("--max", type=int, default=0)
    args = ap.parse_args()

    hf_files = None
    if not args.sin_hf:
        try:
            from huggingface_hub import HfApi
            hf_files = set(HfApi().list_repo_files(HF_REPO, repo_type="dataset"))
            print(f"HF {HF_REPO}: {len(hf_files)} archivos")
        except Exception as e:
            print("No se pudo listar HF:", e)

    rep = {"splits": {}, "escenas": {}}
    escenas = {}
    for split in ("train", "validation", "test"):
        rows = leer_jsonl_tolerante(os.path.join(DATA, f"{split}_multimodal.jsonl"))
        c = collections.Counter()
        for r in rows:
            mm = r.get("multimodal") or {}
            c["filas"] += 1
            c[f"task_{r.get('task_type')}"] += 1
            if not mm.get("image"):
                c["sin_multimodal"] += 1
                continue
            sid = mm["image"].split("/")[1] if "/" in mm["image"] else mm["image"]
            escenas.setdefault(sid, mm)
            if hf_files is not None:
                for k in ("image", "metric_depth", "camera"):
                    if mm.get(k) and mm[k] not in hf_files:
                        c[f"hf_falta_{k}"] += 1
            user0 = next((m["content"] for m in r["messages"] if m["role"] == "user"), "")
            if user0.startswith("<image>") and not mm.get("image"):
                c["token_image_sin_imagen"] += 1
        rep["splits"][split] = dict(c)
        print(split, dict(c))

    ids = sorted(escenas)[: args.max or None]
    print(f"Auditando {len(ids)} escenas únicas...")
    probs = collections.Counter()
    for i, sid in enumerate(ids):
        a = auditar_asset(sid, escenas[sid])
        rep["escenas"][sid] = a
        for p in a["problemas"]:
            probs[p.split(":")[0]] += 1
        if (i + 1) % 500 == 0:
            print(f"  {i + 1}/{len(ids)}", dict(probs), flush=True)
    rep["problemas"] = dict(probs)
    fondo = [a.get("exr_pct_fondo") for a in rep["escenas"].values() if a.get("exr_pct_fondo") is not None]
    rep["exr_pct_fondo_mediana"] = float(np.median(fondo)) if fondo else None
    rep["exr_con_fondo"] = sum(bool(a.get("exr_tiene_fondo")) for a in rep["escenas"].values())
    rep["rgb_tamaños"] = dict(collections.Counter(str(a.get("rgb_size")) for a in rep["escenas"].values()))
    os.makedirs(os.path.join(DATASET, "reports"), exist_ok=True)
    out = os.path.join(DATASET, "reports", "auditoria_multimodal.json")
    json.dump(rep, open(out, "w"), indent=1)
    print("PROBLEMAS:", dict(probs))
    print("EXR con fondo (esperado):", rep["exr_con_fondo"], "| % fondo mediana:", rep["exr_pct_fondo_mediana"])
    print("Tamaños RGB:", rep["rgb_tamaños"])
    print("Reporte:", out)


if __name__ == "__main__":
    main()
