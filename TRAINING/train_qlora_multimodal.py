#!/usr/bin/env python3
"""
train_qlora_multimodal.py
Script avanzado para Fine-Tuning de Qwen2.5-VL (Visión y Lenguaje) usando QLoRA.
Integra Imágenes RGB + Texto -> Código CAD.
"""

import os
import argparse
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
import torch
import json
import numpy as np
from PIL import Image
# Habilitar OpenCV para leer EXR
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2
from torch.utils.data import Dataset
from transformers import (
    Qwen2_5_VLForConditionalGeneration,
    AutoProcessor,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)                 # ASISTENTE-3D
DEFAULT_ASSETS_DIR = os.path.join(PROJECT_DIR, "DATASET")  # contiene images/ y out_assets/
HF_ASSETS_REPO = os.environ.get("HF_ASSETS_REPO", "julianG99/aec-procedural-blender-gold-v2")


def leer_jsonl_tolerante(path):
    """Lee JSONL normal y también archivos con objetos JSON multilínea
    (test_multimodal.jsonl está guardado con indentación)."""
    s = open(path, encoding="utf-8").read()
    dec, i, rows = json.JSONDecoder(), 0, []
    while i < len(s):
        while i < len(s) and s[i] in " \n\t\r,[]":
            i += 1
        if i >= len(s):
            break
        obj, i = dec.raw_decode(s, i)
        rows.append(obj)
    return rows


def descargar_assets(assets_dir, con_profundidad=False):
    """Descarga de Hugging Face el dataset Gold-Standard (images/*, data/*.jsonl) y/o out_assets/*
    a <assets_dir> — las rutas del JSONL son relativas a assets_dir."""
    import shutil
    from huggingface_hub import snapshot_download
    patrones = ["images/*", "data/*.jsonl", "out_assets/*/*_rgb.png"]
    if con_profundidad:
        patrones += ["out_assets/*/*_depth.exr", "out_assets/*/*_camera.json",
                     "out_assets/*/*_depth_est.npz", "out_assets/*/*_depth_est.json"]
    print(f"Descargando assets de {HF_ASSETS_REPO} -> {assets_dir} ({patrones})")
    snapshot_download(repo_id=HF_ASSETS_REPO, repo_type="dataset",
                      local_dir=assets_dir, allow_patterns=patrones, max_workers=16)
    # Sincronizar data/{train,validation,test}.jsonl descargados de HF hacia TRAINING/data/*_multimodal.jsonl
    data_dl = os.path.join(assets_dir, "data")
    train_data_dir = os.path.join(SCRIPT_DIR, "data")
    if os.path.isdir(data_dl):
        os.makedirs(train_data_dir, exist_ok=True)
        for sp in ("train", "validation", "test"):
            src_j = os.path.join(data_dl, f"{sp}.jsonl")
            dst_j = os.path.join(train_data_dir, f"{sp}_multimodal.jsonl")
            if os.path.isfile(src_j):
                shutil.copy2(src_j, dst_j)
                print(f"[ASSETS] Sincronizado {src_j} -> {dst_j}")
    if con_profundidad:
        _reemplazar_assets_viejos(assets_dir)


def _reemplazar_assets_viejos(assets_dir, version_min=2.3):
    """snapshot_download NO sobreescribe archivos que ya existían en local_dir (p.ej. de un
    entrenamiento anterior). Detecta escenas con assets viejos (camera.json sin
    generator_version >= version_min) y fuerza la re-descarga de sus RGB/EXR/cámara."""
    import glob
    from concurrent.futures import ThreadPoolExecutor
    from huggingface_hub import hf_hub_download
    viejas = []
    for cam in glob.glob(os.path.join(assets_dir, "out_assets", "*", "*_camera.json")):
        try:
            v = float(json.load(open(cam)).get("generator_version") or 0)
        except Exception:
            v = 0
        if v < version_min:
            viejas.append(os.path.basename(os.path.dirname(cam)))
    if not viejas:
        print("[ASSETS] Todos los assets locales están en la versión actual.")
        return
    print(f"[ASSETS] {len(viejas)} escenas con assets viejos en {assets_dir}: re-descargando...")

    def bajar(sid):
        for suf in ("_rgb.png", "_depth.exr", "_camera.json"):
            try:
                hf_hub_download(HF_ASSETS_REPO, f"out_assets/{sid}/{sid}{suf}", repo_type="dataset",
                                local_dir=assets_dir, force_download=True)
            except Exception as e:
                print(f"[ASSETS] no se pudo bajar {sid}{suf}: {e}")

    with ThreadPoolExecutor(16) as ex:
        list(ex.map(bajar, viejas))
    print("[ASSETS] Listo.")


def _es_identidad(m):
    try:
        return np.allclose(np.array(m, dtype=float), np.eye(4), atol=1e-6)
    except Exception:
        return False


def texto_camara(path):
    """Texto con datos físicos de la cámara (vacío si el JSON es inválido/identidad)."""
    try:
        cam = json.load(open(path))
        c2w = cam.get("cam_to_world")
        if not c2w or _es_identidad(c2w):
            return ""
        m = np.array(c2w, dtype=float)
        fwd = -m[:3, 2]                              # la cámara mira hacia -Z local
        pitch = np.degrees(np.arcsin(np.clip(fwd[2], -1, 1)))
        K = cam.get("intrinsics") or [[0]]
        W = (cam.get("resolution") or [0])[0]
        fov = np.degrees(2 * np.arctan(W / (2 * K[0][0]))) if K[0][0] else 0
        corte = "; vista de corte sin techo" if cam.get("techo_oculto") else ""
        return (f"\n[Cámara: focal {cam.get('focal_length_mm', 35):.0f} mm, FOV {fov:.0f}°, "
                f"altura {m[2, 3]:.1f} m, inclinación {pitch:.0f}°{corte}]")
    except Exception:
        return ""


def leer_exr(path):
    """EXR → ndarray float32 (H,W[,C]) o None.
    Usa el paquete `OpenEXR` (pip install OpenEXR): OpenCV 5.x de pip NO trae soporte EXR
    (cv2.imread devuelve None en silencio, así fue como el LoRA v2 entrenó sin profundidad).
    OpenCV queda solo como respaldo."""
    try:
        import OpenEXR
        with OpenEXR.File(path) as f:
            ch = f.channels()
            if "RGB" in ch:
                return np.asarray(ch["RGB"].pixels, dtype=np.float32)
            for nombre in ("Z", "V", "R", "Y"):
                if nombre in ch:
                    return np.asarray(ch[nombre].pixels, dtype=np.float32)
            return np.asarray(next(iter(ch.values())).pixels, dtype=np.float32)
    except ImportError:
        pass
    except Exception:
        return None
    return cv2.imread(path, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)


def profundidad_a_imagen(d, valid=None):
    """Profundidad en metros → (PIL RGB claro=cerca, lo, hi). Sin máscara (caso estimado,
    igual que con una foto real) usa percentiles 2–98 para ignorar extremos/fondo."""
    if valid is None:
        valid = np.isfinite(d) & (d > 0)
        if valid.mean() < 0.01:
            return None
        lo, hi = (float(x) for x in np.percentile(d[valid], [2, 98]))
    else:
        lo, hi = float(d[valid].min()), float(d[valid].max())
    norm = np.zeros_like(d, dtype=np.float32)
    dv = np.clip(d[valid], lo, hi)
    norm[valid] = 255.0 * (1.0 - (dv - lo) / max(hi - lo, 1e-6))  # cerca = claro
    return Image.fromarray(norm.astype(np.uint8)).convert("RGB"), lo, hi


def cargar_profundidad_estimada(npz_path, escala=None):
    """Profundidad monocular (Depth Anything, DATASET/scripts/estimar_profundidad.py)
    escalada con el ancla métrica. escala=None → usa escala_ancla del .json (si existe)."""
    try:
        d = np.load(npz_path)["depth"].astype(np.float32)
    except Exception:
        return None
    if escala is None:
        try:
            escala = json.load(open(npz_path.replace(".npz", ".json"))).get("escala_ancla", 1.0)
        except Exception:
            escala = 1.0
    return profundidad_a_imagen(d * float(escala))


def cargar_profundidad(path):
    """EXR métrico → (PIL RGB normalizada claro=cerca, min_m, max_m) o None si no es un pase Z válido."""
    d = leer_exr(path)
    if d is None:
        return None
    if d.ndim == 3:
        # Un pase Z real tiene los 3 canales iguales; si difieren es un render RGB (assets viejos).
        if not (np.allclose(d[..., 0], d[..., 1]) and np.allclose(d[..., 1], d[..., 2])):
            return None
        d = d[..., 0]
    valid = np.isfinite(d) & (d > 0) & (d < 1e4)
    if valid.mean() < 0.01:
        return None
    lo, hi = float(d[valid].min()), float(d[valid].max())
    norm = np.zeros_like(d, dtype=np.float32)
    norm[valid] = 255.0 * (1.0 - (d[valid] - lo) / max(hi - lo, 1e-6))  # cerca = claro
    return Image.fromarray(norm.astype(np.uint8)).convert("RGB"), lo, hi


class QwenVLDataset(Dataset):
    """Dataset Custom para cargar el JSONL Multimodal.

    - Las rutas de `multimodal` son relativas a `assets_dir` (DATASET/).
    - La imagen va SOLO en el primer turno de usuario.
    - La loss se calcula sobre TODOS los turnos del assistant (multi-turno incluido).
    - Profundidad y cámara ACTIVADAS por defecto (assets generator_version ≥ 2.1,
      DATASET/scripts/generate_multimodal_assets.py). Si detecta EXR viejos (copia
      del RGB, bug previo) o cámaras identidad, los descarta y avisa.
    """
    def __init__(self, jsonl_path, processor, max_length=6144, assets_dir=DEFAULT_ASSETS_DIR,
                 usar_profundidad=True, usar_camara=True, fuente_profundidad="estimada",
                 aumentar=False, ruido_escala=0.15, p_sin_profundidad=0.0, p_sin_camara=0.0):
        """fuente_profundidad: 'gt' (EXR de Blender, exacto) o 'estimada' (Depth Anything +
        ancla métrica: lo que habrá en inferencia con fotos reales).
        aumentar=True (solo train): ruido multiplicativo de ±ruido_escala sobre el ancla
        (simula una medida del usuario imprecisa) y dropout de profundidad / cámara."""
        import random
        self._rng = random.Random(1234)
        self.fuente_profundidad = fuente_profundidad
        self.aumentar = aumentar
        self.ruido_escala = ruido_escala
        self.p_sin_profundidad = p_sin_profundidad
        self.p_sin_camara = p_sin_camara
        self.processor = processor
        self.max_length = max_length
        self.assets_dir = assets_dir
        self.usar_profundidad = usar_profundidad
        self.usar_camara = usar_camara
        tok = processor.tokenizer
        self.assistant_prefix = tok.encode("<|im_start|>assistant\n", add_special_tokens=False)
        self.im_end_id = tok.convert_tokens_to_ids("<|im_end|>")
        self.data = leer_jsonl_tolerante(jsonl_path)

        # Resolver rutas una sola vez y reportar cobertura (soporta tanto multimodal.image como image en raíz)
        n_img = n_ref = n_depth = n_ref_depth = 0
        for item in self.data:
            mm = item.get("multimodal") or {}
            img_rel = mm.get("image") if mm.get("image") is not None else item.get("image")
            item["_img"] = self._resolver(img_rel)
            dep = mm.get("metric_depth")
            if dep and fuente_profundidad == "estimada":
                dep = dep.replace("_depth.exr", "_depth_est.npz")
            item["_depth"] = self._resolver(dep) if usar_profundidad else None
            item["_cam"] = self._resolver(mm.get("camera")) if usar_camara else None
            n_ref += bool(img_rel)
            n_img += bool(item["_img"])
            n_ref_depth += bool(dep)
            n_depth += bool(item["_depth"])
        self.n_con_imagen = n_img
        print(f"[DATA] {os.path.basename(jsonl_path)}: {len(self.data)} ejemplos | "
              f"con imagen RGB encontrada: {n_img}/{n_ref} referenciadas"
              + (f" | profundidad ({fuente_profundidad}): {n_depth}/{n_ref_depth}" if usar_profundidad else "")
              + (f" | aumentos: ruido escala ±{ruido_escala:.0%}, sin prof. {p_sin_profundidad:.0%}, "
                 f"sin cámara {p_sin_camara:.0%}" if aumentar else ""))

        # Verificación real: si el dataset referencia mapas de profundidad, exigir que >=90% sean legibles
        if usar_profundidad and n_depth:
            muestra = [it["_depth"] for it in self.data if it["_depth"]][:: max(1, n_depth // 40)][:40]
            ok = sum(self._cargar_profundidad(p) is not None for p in muestra)
            print(f"[DATA] Profundidades legibles en muestra: {ok}/{len(muestra)}")
            if ok < 0.9 * len(muestra):
                raise SystemExit(
                    f"[ERROR] Solo {ok}/{len(muestra)} mapas de profundidad se pudieron leer. "
                    "EXR: pip install OpenEXR (OpenCV 5 no lee EXR). Estimada: faltan *_depth_est.npz "
                    "(--descargar_assets). Para entrenar sin profundidad a propósito: --no-usar_profundidad")
        if usar_profundidad and n_ref_depth > 0 and n_depth < 0.9 * n_ref_depth:
            raise SystemExit(f"[ERROR] Solo {n_depth}/{n_ref_depth} ejemplos tienen archivo de profundidad "
                             f"({fuente_profundidad}). ¿Falta --descargar_assets?")

    def _resolver(self, rel):
        if not rel:
            return None
        for cand in (os.path.join(self.assets_dir, rel), rel):
            if os.path.isfile(cand):
                return cand
        return None

    def __len__(self):
        return len(self.data)

    def _cargar_profundidad(self, path, ruido=1.0):
        if path.endswith(".npz"):
            try:
                escala = json.load(open(path.replace(".npz", ".json"))).get("escala_ancla", 1.0)
            except Exception:
                escala = 1.0
            return cargar_profundidad_estimada(path, escala * ruido)
        return cargar_profundidad(path)

    def __getitem__(self, idx):
        item = self.data[idx]
        messages = item["messages"]

        # 1) Cargar imágenes ANTES de armar el texto: así nunca hay un placeholder
        #    <image> sin su imagen (eso hace fallar al processor).
        bloques = []   # (texto_intro, PIL.Image)
        if item.get("_img"):
            try:
                bloques.append(("Fotografía de referencia (RGB):",
                                Image.open(item["_img"]).convert("RGB")))
            except Exception as e:
                print(f"[WARN] {item.get('id')}: RGB ilegible ({e})")
        rng = self._rng
        quitar_prof = self.aumentar and rng.random() < self.p_sin_profundidad
        quitar_cam = self.aumentar and rng.random() < self.p_sin_camara
        if item.get("_depth") and not quitar_prof:
            ruido = 1.0
            if self.aumentar and self.ruido_escala > 0:
                ruido = float(np.exp(rng.uniform(-np.log1p(self.ruido_escala), np.log1p(self.ruido_escala))))
            res = self._cargar_profundidad(item["_depth"], ruido)
            if res is not None:
                dimg, lo, hi = res
                if item["_depth"].endswith(".npz"):
                    intro = f"Mapa de profundidad estimada (claro = cerca; rango aprox. {lo:.1f}–{hi:.1f} m):"
                else:
                    intro = f"Mapa de profundidad métrica (claro = cerca; rango {lo:.1f}–{hi:.1f} m):"
                bloques.append((intro, dimg))
            else:
                self._n_depth_mala = getattr(self, "_n_depth_mala", 0) + 1
                if self._n_depth_mala <= 5:
                    print(f"[WARN] {item.get('id')}: profundidad ilegible ({item['_depth']}), se omite")
        camera_info = texto_camara(item["_cam"]) if item.get("_cam") and not quitar_cam else ""

        qwen_messages, primer_user = [], True
        for msg in messages:
            if msg["role"] == "user":
                content = []
                if primer_user:
                    for texto, _ in bloques:
                        content.append({"type": "text", "text": texto})
                        content.append({"type": "image"})
                clean_text = msg["content"].replace("<image>\n", "").replace("<image>", "").strip()
                extra = camera_info if primer_user else ""
                content.append({"type": "text", "text": f"Instrucción del usuario: {clean_text}{extra}"})
                qwen_messages.append({"role": "user", "content": content})
                primer_user = False
            elif msg["role"] == "assistant":
                # Compactar comentarios puros y líneas vacías dentro del bloque python para ahorrar ~35% de tokens sin perder código
                raw_c = msg["content"]
                if "```python\n" in raw_c:
                    pref, rest = raw_c.split("```python\n", 1)
                    code_b, suff = rest.split("```", 1)
                    compact_lines = [
                        ln.rstrip() for ln in code_b.splitlines()
                        if ln.strip() and not ln.strip().startswith("#")
                    ]
                    raw_c = f"{pref}```python\n" + "\n".join(compact_lines) + f"\n```{suff}"
                qwen_messages.append({"role": "assistant", "content": [{"type": "text", "text": raw_c}]})
            else:
                qwen_messages.append({"role": msg["role"], "content": [{"type": "text", "text": msg["content"]}]})

        text_prompt = self.processor.apply_chat_template(qwen_messages, tokenize=False, add_generation_prompt=False)
        image_inputs = [img for _, img in bloques]

        # Tokenizar (Text + Imagen) SIN padding ni truncado: el collator hace
        # padding dinámico. Truncar aquí podía cortar tokens de imagen o el código.
        inputs = self.processor(
            text=[text_prompt],
            images=image_inputs if image_inputs else None,
            padding=False,
            return_tensors="pt"
        )
        inputs = {k: v.squeeze(0) if k in ("input_ids", "attention_mask") else v
                  for k, v in inputs.items()}

        input_ids = inputs["input_ids"]
        labels = torch.full_like(input_ids, -100)

        # Loss solo sobre las respuestas del assistant (todas, incluido <|im_end|>).
        ids = input_ids.tolist()
        n = len(self.assistant_prefix)
        encontrados = 0
        i = 0
        while i <= len(ids) - n:
            if ids[i:i + n] == self.assistant_prefix:
                ini = i + n
                fin = ini
                while fin < len(ids) and ids[fin] != self.im_end_id:
                    fin += 1
                fin = min(fin + 1, len(ids))   # incluir <|im_end|> para aprender a parar
                labels[ini:fin] = input_ids[ini:fin]
                encontrados += 1
                i = fin
            else:
                i += 1
        if not encontrados:
            print(f"[WARN] item {item.get('id')}: no se encontró el turno del assistant")

        # Truncado seguro: solo recorta la cola (código), nunca los tokens de imagen
        if input_ids.shape[0] > self.max_length:
            n_trunc = getattr(self, "_n_trunc", 0) + 1
            self._n_trunc = n_trunc
            if n_trunc <= 20:
                print(f"[WARN] item {item.get('id')}: {input_ids.shape[0]} tokens > "
                      f"{self.max_length}, se trunca la cola del código")
            inputs["input_ids"] = input_ids[:self.max_length]
            inputs["attention_mask"] = inputs["attention_mask"][:self.max_length]
            labels = labels[:self.max_length]

        inputs["labels"] = labels
        return inputs


def _find_last_subseq(seq, sub):
    n = len(sub)
    for i in range(len(seq) - n, -1, -1):
        if seq[i:i + n] == sub:
            return i
    return None


class QwenVLCollator:
    """Padding dinámico. pixel_values/image_grid_thw se CONCATENAN (formato Qwen2.5-VL),
    no se apilan; los labels de padding van a -100."""
    def __init__(self, pad_token_id):
        self.pad_token_id = pad_token_id

    def __call__(self, features):
        max_len = max(f["input_ids"].shape[0] for f in features)
        batch = {"input_ids": [], "attention_mask": [], "labels": []}
        for f in features:
            pad = max_len - f["input_ids"].shape[0]
            batch["input_ids"].append(torch.nn.functional.pad(f["input_ids"], (0, pad), value=self.pad_token_id))
            batch["attention_mask"].append(torch.nn.functional.pad(f["attention_mask"], (0, pad), value=0))
            batch["labels"].append(torch.nn.functional.pad(f["labels"], (0, pad), value=-100))
        batch = {k: torch.stack(v) for k, v in batch.items()}
        for key in ("pixel_values", "image_grid_thw"):
            vals = [f[key] for f in features if key in f]
            if vals:
                batch[key] = torch.cat(vals, dim=0)
        return batch


class ChunkedCrossEntropyTrainer(Trainer):
    """Evita materializar la matriz gigante de logits [B, seq_len, 152064] (que consume ~18 GB
    entre bf16 y los 20 chunks de 594 MB guardados en el grafo autograd).
    Intercepta lm_head durante el forward para recibir hidden_states [B, seq_len, D] (~110 MB)
    y calcula lm_head + cross_entropy en bloques de 512 tokens con gradient checkpointing,
    usando solo ~290 MB de VRAM pico."""

    @staticmethod
    def _find_lm_head_holders(model):
        holders = []
        if hasattr(model, "modules"):
            for m in model.modules():
                mods = getattr(m, "_modules", None)
                if isinstance(mods, dict) and "lm_head" in mods and mods["lm_head"] is not None:
                    holders.append(m)
        if not holders:
            for obj in (
                getattr(getattr(model, "base_model", None), "model", None),
                getattr(model, "base_model", None),
                getattr(model, "model", None),
                model,
            ):
                if obj is not None and hasattr(obj, "lm_head") and getattr(obj, "lm_head") is not None:
                    holders.append(obj)
                    break
        return holders

    def compute_loss(self, model, inputs, return_outputs=False, num_items_in_batch=None):
        labels = inputs.get("labels")
        if labels is None:
            return super().compute_loss(model, inputs, return_outputs=return_outputs)

        model_inputs = {k: v for k, v in inputs.items() if k != "labels"}
        holders = self._find_lm_head_holders(model)
        real_lm_head = getattr(holders[0], "lm_head", None) if holders else None

        if real_lm_head is not None and hasattr(torch.nn, "Identity"):
            identity_mod = torch.nn.Identity()
            try:
                for h_obj in holders:
                    setattr(h_obj, "lm_head", identity_mod)
                outputs = model(**model_inputs)
            finally:
                for h_obj in holders:
                    setattr(h_obj, "lm_head", real_lm_head)
            hidden = outputs.get("logits") if isinstance(outputs, dict) else outputs.logits
            shift_hidden = hidden[..., :-1, :]
            shift_labels = labels[..., 1:]

            valid_mask = shift_labels != -100
            total_valid = valid_mask.sum()
            if int(total_valid.item()) == 0:
                loss = shift_hidden.sum() * 0.0
                return (loss, outputs) if return_outputs else loss

            in_features = getattr(real_lm_head, "in_features", None)

            def _chunk_ce(h_chunk, y_chunk):
                if in_features is None or h_chunk.shape[-1] == in_features:
                    logits_chunk = real_lm_head(h_chunk).float()
                else:
                    logits_chunk = h_chunk.float()
                return torch.nn.functional.cross_entropy(
                    logits_chunk.reshape(-1, logits_chunk.shape[-1]),
                    y_chunk.reshape(-1),
                    ignore_index=-100,
                    reduction="sum",
                )

            seq_len = shift_hidden.shape[1]
            chunk_size = 512
            loss_sum = None
            use_ckpt = hasattr(torch.utils, "checkpoint") and hasattr(torch.utils.checkpoint, "checkpoint")
            for start in range(0, seq_len, chunk_size):
                end = min(start + chunk_size, seq_len)
                y_sub = shift_labels[:, start:end]
                if not bool((y_sub != -100).any().item()):
                    continue
                h_sub = shift_hidden[:, start:end, :]
                if use_ckpt and getattr(model, "training", False):
                    step_loss = torch.utils.checkpoint.checkpoint(
                        _chunk_ce, h_sub, y_sub, use_reentrant=False
                    )
                else:
                    step_loss = _chunk_ce(h_sub, y_sub)
                loss_sum = step_loss if loss_sum is None else (loss_sum + step_loss)

            loss = (loss_sum / total_valid) if loss_sum is not None else (shift_hidden.sum() * 0.0)
            return (loss, outputs) if return_outputs else loss

        # Fallback cuando el modelo no expone lm_head (ej. mocks en tests unitarios)
        outputs = model(**model_inputs)
        logits = outputs.get("logits") if isinstance(outputs, dict) else outputs.logits
        shift_logits = logits[..., :-1, :]
        shift_labels = labels[..., 1:]
        valid_mask = shift_labels != -100
        total_valid = valid_mask.sum()
        if int(total_valid.item()) == 0:
            loss = shift_logits.sum() * 0.0
            return (loss, outputs) if return_outputs else loss

        seq_len = shift_logits.shape[1]
        chunk_size = 512
        loss_sum = None
        for start in range(0, seq_len, chunk_size):
            end = min(start + chunk_size, seq_len)
            sub_labels = shift_labels[:, start:end].reshape(-1)
            if not bool((sub_labels != -100).any().item()):
                continue
            sub_logits = shift_logits[:, start:end, :].reshape(-1, shift_logits.shape[-1]).float()
            step_loss = torch.nn.functional.cross_entropy(
                sub_logits, sub_labels, ignore_index=-100, reduction="sum"
            )
            loss_sum = step_loss if loss_sum is None else (loss_sum + step_loss)

        loss = (loss_sum / total_valid) if loss_sum is not None else (shift_logits.sum() * 0.0)
        return (loss, outputs) if return_outputs else loss


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name_or_path", type=str, default="Qwen/Qwen2.5-VL-7B-Instruct")
    parser.add_argument("--train_file", type=str, default=os.path.join(PROJECT_DIR, "TRAINING/data/train_multimodal.jsonl"))
    parser.add_argument("--val_file", type=str, default=os.path.join(PROJECT_DIR, "TRAINING/data/validation_multimodal.jsonl"))
    parser.add_argument("--output_dir", type=str, default="./checkpoints")
    parser.add_argument("--batch_size", type=int, default=1, help="Usa 1 para A100 40GB / L4 (24GB). Usa 2 para A100 80GB.")
    parser.add_argument("--push_to_hub", action="store_true", help="Subir el adaptador LoRA a Hugging Face al terminar")
    parser.add_argument("--hub_model_id", type=str, default="julianG99/qwen2.5-vl-aec-lora-gold-v1", help="Ej: tu_usuario/qwen2.5-vl-aec-lora")
    parser.add_argument("--max_length", type=int, default=14336, help="Tokens máximos por ejemplo (con compactación de comentarios y checkpointed lm_head cubre el código completo en A100 40GB)")
    parser.add_argument("--assets_dir", type=str, default=DEFAULT_ASSETS_DIR,
                        help="Carpeta que contiene images/ y out_assets/ (rutas del JSONL son relativas a ella)")
    parser.add_argument("--descargar_assets", action="store_true",
                        help=f"Descargar renders desde HF ({HF_ASSETS_REPO}) a --assets_dir antes de entrenar")
    parser.add_argument("--usar_profundidad", action=argparse.BooleanOptionalAction, default=False,
                        help="Incluir mapa de profundidad métrica EXR como 2ª imagen (desactivado por defecto en Gold-Standard RGB)")
    parser.add_argument("--usar_camara", action=argparse.BooleanOptionalAction, default=False,
                        help="Incluir datos de cámara como texto (desactivado por defecto en Gold-Standard RGB)")
    parser.add_argument("--min_pct_imagenes", type=float, default=0.5,
                        help="Aborta si menos de esta fracción de ejemplos tiene imagen (0.5 soporta Modality Dropout). 0 = desactivar")
    parser.add_argument("--max_pixels", type=int, default=768 * 768, help="Resolución máxima por imagen (controla tokens visuales)")
    parser.add_argument("--num_epochs", type=float, default=2)
    parser.add_argument("--max_steps", type=int, default=-1, help="Para pruebas rápidas (smoke test)")
    parser.add_argument("--report_to", type=str, default="wandb", help="wandb | none")
    parser.add_argument("--lora_r", type=int, default=64, help="Rango LoRA (alpha = 2*r)")
    parser.add_argument("--save_steps", type=int, default=50,
                        help="Si >0: evalúa y guarda checkpoint cada N pasos (en vez de por época), "
                             "para no perder progreso si se cae")
    parser.add_argument("--resume_from_checkpoint", type=str, default=None,
                        help="Ruta a checkpoint-XXX (o 'last' = el más reciente en output_dir)")
    parser.add_argument("--fuente_profundidad", choices=["estimada", "gt"], default="estimada",
                        help="estimada = Depth Anything + ancla métrica (como en inferencia); gt = EXR de Blender")
    parser.add_argument("--ruido_escala", type=float, default=0.15,
                        help="Ruido ± sobre el ancla métrica en train (medida del usuario imprecisa)")
    parser.add_argument("--p_sin_profundidad", type=float, default=0.15,
                        help="Prob. de quitar el mapa de profundidad en un ejemplo de train")
    parser.add_argument("--p_sin_camara", type=float, default=0.15,
                        help="Prob. de quitar el texto de cámara en un ejemplo de train")
    args = parser.parse_args()

    if args.descargar_assets or not os.path.isdir(os.path.join(args.assets_dir, "images")):
        descargar_assets(args.assets_dir, con_profundidad=args.usar_profundidad or args.usar_camara)

    # Configurar Quantización (4-bits) para que quepa en memoria
    print("Configurando BitsAndBytes (4-bits)...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    # Cargar Procesador y Modelo Base
    print(f"Cargando Modelo {args.model_name_or_path}...")
    processor = AutoProcessor.from_pretrained(args.model_name_or_path,
                                              min_pixels=128 * 28 * 28, max_pixels=args.max_pixels)
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        args.model_name_or_path,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.bfloat16
    )
    model.config.use_cache = False
    model = prepare_model_for_kbit_training(
        model, use_gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False})

    # LoRA (Fine-Tuning Adaptativo)
    print("Configurando LoRA Multimodal...")
    # Ojo: estos nombres también coinciden con el MLP del encoder visual (gate/up/down_proj),
    # así que el LoRA adapta el LLM y, en menor medida, la parte visual.
    peft_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=2 * args.lora_r,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"], 
        lora_dropout=0.1, # Aumentado de 0.05 a 0.10 para evitar memorización
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    # Datasets
    print("Cargando y procesando Datasets (Esto puede tomar tiempo)...")
    ds_kw = dict(max_length=args.max_length, assets_dir=args.assets_dir,
                 usar_profundidad=args.usar_profundidad, usar_camara=args.usar_camara)
    ds_kw["fuente_profundidad"] = args.fuente_profundidad
    train_dataset = QwenVLDataset(args.train_file, processor, aumentar=True, ruido_escala=args.ruido_escala,
                                  p_sin_profundidad=args.p_sin_profundidad, p_sin_camara=args.p_sin_camara,
                                  **ds_kw)
    val_dataset = QwenVLDataset(args.val_file, processor, **ds_kw)
    pct = train_dataset.n_con_imagen / max(1, len(train_dataset))
    if pct < args.min_pct_imagenes:
        raise SystemExit(
            f"[ERROR] Solo {pct:.0%} de los ejemplos de train tienen imagen en '{args.assets_dir}'. "
            f"Usa --descargar_assets (o --assets_dir correcto). Para entrenar solo-texto a propósito: --min_pct_imagenes 0")

    # Determinar si la GPU soporta BFloat16 (Ampere o superior como A100, L4, RTX 3090+)
    # Si es una T4 (Turing) o anterior, se fuerza a usar FP16 estándar.
    use_bf16 = torch.cuda.is_bf16_supported() if torch.cuda.is_available() else False
    use_fp16 = not use_bf16
    print(f"Hardware Compute Type: {'BFloat16' if use_bf16 else 'Float16 (T4/Antiguas)'}")

    # Trainer
    grad_acc = 16 // args.batch_size # Mantiene el batch efectivo total en 16
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.num_epochs,  # 2 por defecto para evitar overfitting post-paso 400
        max_steps=args.max_steps,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=1,  
        gradient_accumulation_steps=grad_acc,
        eval_accumulation_steps=2,     
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},  # evita "Gradients will be None" con QLoRA
        optim="paged_adamw_32bit",
        learning_rate=1e-4,            # Bajado de 2e-4 a 1e-4 para una caída más suave
        weight_decay=0.01,             # Penalización para evitar memorización bruta
        bf16=use_bf16,
        fp16=use_fp16,
        bf16_full_eval=use_bf16,       
        fp16_full_eval=use_fp16,
        logging_steps=10,
        eval_strategy="steps" if args.save_steps > 0 else "epoch",
        save_strategy="steps" if args.save_steps > 0 else "epoch",
        eval_steps=args.save_steps if args.save_steps > 0 else None,
        save_steps=args.save_steps if args.save_steps > 0 else 500,
        save_total_limit=3,
        metric_for_best_model="eval_loss",
        load_best_model_at_end=True,   # Garantiza que el modelo final sea el mejor, no el último
        remove_unused_columns=False, 
        report_to=args.report_to
    )

    trainer = ChunkedCrossEntropyTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=QwenVLCollator(processor.tokenizer.pad_token_id),
        callbacks=[EarlyStoppingCallback(early_stopping_patience=1)] # Se detiene si el eval/loss sube en 1 época
    )

    print("Iniciando Entrenamiento...")
    resume = args.resume_from_checkpoint
    if resume == "last":
        resume = True  # Trainer busca el checkpoint más reciente en output_dir
    trainer.train(resume_from_checkpoint=resume)
    
    # Guardar Modelo
    trainer.model.save_pretrained(os.path.join(args.output_dir, "final_qwen_vl_lora"))
    processor.save_pretrained(os.path.join(args.output_dir, "final_qwen_vl_lora"))
    print("Entrenamiento Multimodal Finalizado y Adapters Guardados Localmente.")

    if args.push_to_hub and args.hub_model_id:
        print(f"Subiendo los adaptadores LoRA a Hugging Face Hub: {args.hub_model_id}...")
        try:
            trainer.model.push_to_hub(args.hub_model_id, private=False)
            processor.push_to_hub(args.hub_model_id, private=False)
            print("Modelos subidos exitosamente al Hub.")
        except Exception as e:
            print(f"Error al subir al Hub: {e}")

if __name__ == "__main__":
    main()
