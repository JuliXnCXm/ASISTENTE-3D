#!/usr/bin/env python3
"""
benchmark_depth.py
Compara estimadores monoculares de profundidad MÉTRICA (familia Depth Anything)
contra la profundidad real de Blender (EXR, pase Z en metros).

Métricas (sobre píxeles con geometría):
  AbsRel  = mean(|pred-gt|/gt)            (menor es mejor)
  delta1  = % píxeles con max(pred/gt, gt/pred) < 1.25   (mayor es mejor)
  escala  = mediana(pred/gt)              (1.0 = escala correcta)
  AbsRel_med = AbsRel tras alinear por la mediana (solo forma, sin error de escala)

Uso:
  python DATASET/tools/benchmark_depth.py --n 120 --modelos v2-indoor-l v2-outdoor-l
Salida: DATASET/reports/benchmark_depth.json
"""
import os, sys, json, argparse, random, time
import numpy as np
import torch
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "TRAINING"))
from train_qlora_multimodal import leer_exr, leer_jsonl_tolerante  # noqa: E402

MODELOS = {
    "v2-indoor-l": "depth-anything/Depth-Anything-V2-Metric-Indoor-Large-hf",
    "v2-outdoor-l": "depth-anything/Depth-Anything-V2-Metric-Outdoor-Large-hf",
    "v2-indoor-s": "depth-anything/Depth-Anything-V2-Metric-Indoor-Small-hf",
    "v2-outdoor-s": "depth-anything/Depth-Anything-V2-Metric-Outdoor-Small-hf",
}


def escenas(n, seed=0):
    vistos, out = set(), []
    for sp in ("train", "validation"):
        for r in leer_jsonl_tolerante(os.path.join(ROOT, "TRAINING", "data", f"{sp}_multimodal.jsonl")):
            mm = r.get("multimodal") or {}
            if mm.get("metric_depth") and mm["image"] not in vistos:
                vistos.add(mm["image"])
                out.append(mm)
    random.Random(seed).shuffle(out)
    return out[:n]


def metricas(pred, gt):
    m = np.isfinite(gt) & (gt > 0) & (gt < 1e4) & np.isfinite(pred) & (pred > 0)
    if m.mean() < 0.01:
        return None
    p, g = pred[m], gt[m]
    s = float(np.median(p / g))
    ps = p / s
    r = np.maximum(p / g, g / p)
    return dict(absrel=float(np.mean(np.abs(p - g) / g)), delta1=float((r < 1.25).mean()),
                escala=s, absrel_med=float(np.mean(np.abs(ps - g) / g)),
                gt_max=float(g.max()))


class EstimadorV2:
    def __init__(self, repo, device):
        from transformers import AutoImageProcessor, AutoModelForDepthEstimation
        self.proc = AutoImageProcessor.from_pretrained(repo)
        self.model = AutoModelForDepthEstimation.from_pretrained(repo).to(device).eval()
        self.device = device

    @torch.no_grad()
    def __call__(self, img):
        x = self.proc(images=img, return_tensors="pt")
        d = self.model(pixel_values=x["pixel_values"].to(self.device)).predicted_depth
        d = torch.nn.functional.interpolate(d[:, None].float(), size=img.size[::-1],
                                            mode="bicubic", align_corners=False)[0, 0]
        return d.cpu().numpy()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=120)
    ap.add_argument("--modelos", nargs="+", default=["v2-indoor-l", "v2-outdoor-l"])
    args = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    data = escenas(args.n)
    gts = []
    for mm in data:
        gt = leer_exr(os.path.join(ROOT, "DATASET", mm["metric_depth"]))
        gt = gt[..., 0] if gt is not None and gt.ndim == 3 else gt
        cam = json.load(open(os.path.join(ROOT, "DATASET", mm["camera"])))
        gts.append((mm, gt, bool(cam.get("techo_oculto"))))

    rep = {}
    for nombre in args.modelos:
        est = EstimadorV2(MODELOS[nombre], device)
        filas, t0 = [], time.time()
        for mm, gt, interior in gts:
            img = Image.open(os.path.join(ROOT, "DATASET", mm["image"])).convert("RGB")
            m = metricas(est(img), gt)
            if m:
                m.update(escena=mm["image"].split("/")[1], interior=interior)
                filas.append(m)
        dt = (time.time() - t0) / max(1, len(filas))
        del est
        torch.cuda.empty_cache()

        def resumen(fs):
            if not fs:
                return {}
            return {k: round(float(np.median([f[k] for f in fs])), 3)
                    for k in ("absrel", "delta1", "escala", "absrel_med")} | {"n": len(fs)}
        grupos = {"todas": filas,
                  "interior(corte)": [f for f in filas if f["interior"]],
                  "exterior": [f for f in filas if not f["interior"]],
                  "lejos(>40m)": [f for f in filas if f["gt_max"] > 40]}
        rep[nombre] = {g: resumen(fs) for g, fs in grupos.items()} | {"seg_por_imagen": round(dt, 3)}
        print(f"\n== {nombre} ({dt:.2f}s/img)")
        for g, r in rep[nombre].items():
            print(f"  {g:16s} {r}")
        rep[nombre]["filas"] = filas

    out = os.path.join(ROOT, "DATASET", "reports", "benchmark_depth.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(rep, open(out, "w"), indent=1)
    print("\nReporte:", out)


if __name__ == "__main__":
    main()
