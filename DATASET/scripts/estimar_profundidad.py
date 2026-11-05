#!/usr/bin/env python3
"""
estimar_profundidad.py
Genera la profundidad ESTIMADA (monocular) de cada render RGB del dataset con
Depth Anything V2 Metric (Indoor-Large por defecto), es decir, lo mismo que se
podrá calcular en inferencia a partir de una foto del usuario.

Por escena guarda:
  out_assets/<sid>/<sid>_depth_est.npz   depth float16 (H,W) en "metros del modelo"
  out_assets/<sid>/<sid>_depth_est.json  {modelo, escala_ancla, absrel_alineado, ...}

escala_ancla = mediana(gt / pred) usando el EXR real: simula el "ancla métrica"
(una medida conocida que da el usuario). En entrenamiento se aplica con ruido.

Uso:
  python DATASET/scripts/estimar_profundidad.py [--modelo depth-anything/...] [--saltar_existentes]
"""
import os, sys, json, argparse, time
import numpy as np
import torch
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "TRAINING"))
from train_qlora_multimodal import leer_exr, leer_jsonl_tolerante  # noqa: E402

MODELO_DEF = "depth-anything/Depth-Anything-V2-Metric-Indoor-Large-hf"


class Estimador:
    def __init__(self, repo, device="cuda"):
        from transformers import AutoImageProcessor, AutoModelForDepthEstimation
        self.repo = repo
        self.proc = AutoImageProcessor.from_pretrained(repo)
        self.model = AutoModelForDepthEstimation.from_pretrained(repo).to(device).eval()
        self.device = device

    @torch.no_grad()
    def __call__(self, img):
        x = self.proc(images=img, return_tensors="pt")
        d = self.model(pixel_values=x["pixel_values"].to(self.device)).predicted_depth
        d = torch.nn.functional.interpolate(d[:, None].float(), size=img.size[::-1],
                                            mode="bicubic", align_corners=False)[0, 0]
        return d.clamp(min=1e-3).cpu().numpy()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelo", default=MODELO_DEF)
    ap.add_argument("--saltar_existentes", action="store_true")
    args = ap.parse_args()

    escenas = {}
    for sp in ("train", "validation", "test"):
        for r in leer_jsonl_tolerante(os.path.join(ROOT, "TRAINING", "data", f"{sp}_multimodal.jsonl")):
            mm = r.get("multimodal") or {}
            if mm.get("image"):
                escenas[mm["image"].split("/")[1]] = mm
    print(f"{len(escenas)} escenas | modelo {args.modelo}")
    est = Estimador(args.modelo)
    t0, n, errs = time.time(), 0, []
    for i, (sid, mm) in enumerate(sorted(escenas.items())):
        base = os.path.join(ROOT, "DATASET", "out_assets", sid, sid)
        if args.saltar_existentes and os.path.exists(base + "_depth_est.json"):
            continue
        img = Image.open(os.path.join(ROOT, "DATASET", mm["image"])).convert("RGB")
        pred = est(img)
        meta = {"modelo": args.modelo, "forma": list(pred.shape)}
        gt = leer_exr(os.path.join(ROOT, "DATASET", mm["metric_depth"])) if mm.get("metric_depth") else None
        if gt is not None:
            gt = gt[..., 0] if gt.ndim == 3 else gt
            m = np.isfinite(gt) & (gt > 0) & (gt < 1e4)
            if m.mean() > 0.005:
                s = float(np.median(gt[m] / pred[m]))
                meta["escala_ancla"] = s
                meta["absrel_alineado"] = float(np.mean(np.abs(pred[m] * s - gt[m]) / gt[m]))
                errs.append(meta["absrel_alineado"])
        np.savez_compressed(base + "_depth_est.npz", depth=pred.astype(np.float16))
        json.dump(meta, open(base + "_depth_est.json", "w"))
        n += 1
        if (i + 1) % 250 == 0:
            print(f"  {i + 1}/{len(escenas)}  {(time.time() - t0) / n:.2f}s/img  "
                  f"AbsRel alineado mediana {np.median(errs):.3f}", flush=True)
    print(f"Listo: {n} escenas en {time.time() - t0:.0f}s | AbsRel alineado mediana "
          f"{np.median(errs) if errs else float('nan'):.3f}")


if __name__ == "__main__":
    main()
