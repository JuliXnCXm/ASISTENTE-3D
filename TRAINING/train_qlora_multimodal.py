#!/usr/bin/env python3
"""
train_qlora_multimodal.py
Script avanzado para Fine-Tuning de Qwen2.5-VL (Visión y Lenguaje) usando QLoRA.
Integra Imágenes RGB + Texto -> Código CAD.
"""

import os
import argparse
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
DEFAULT_ASSETS_DIR = os.path.join(PROJECT_DIR, "DATASET")  # contiene out_assets/
HF_ASSETS_REPO = "julianG99/aec-procedural-blender"


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
    """Descarga de Hugging Face SOLO lo necesario (renders RGB; EXR/cámara opcional)
    a <assets_dir>/out_assets/... — las rutas del JSONL son relativas a assets_dir."""
    from huggingface_hub import snapshot_download
    patrones = ["out_assets/*/*_rgb.png"]
    if con_profundidad:
        patrones += ["out_assets/*/*_depth.exr", "out_assets/*/*_camera.json"]
    print(f"Descargando assets de {HF_ASSETS_REPO} -> {assets_dir} ({patrones})")
    snapshot_download(repo_id=HF_ASSETS_REPO, repo_type="dataset",
                      local_dir=assets_dir, allow_patterns=patrones, max_workers=16)
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


def cargar_profundidad(path):
    """EXR métrico → (PIL RGB normalizada claro=cerca, min_m, max_m) o None si no es un pase Z válido."""
    d = cv2.imread(path, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
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
                 usar_profundidad=True, usar_camara=True):
        self.processor = processor
        self.max_length = max_length
        self.assets_dir = assets_dir
        self.usar_profundidad = usar_profundidad
        self.usar_camara = usar_camara
        tok = processor.tokenizer
        self.assistant_prefix = tok.encode("<|im_start|>assistant\n", add_special_tokens=False)
        self.im_end_id = tok.convert_tokens_to_ids("<|im_end|>")
        self.data = leer_jsonl_tolerante(jsonl_path)

        # Resolver rutas una sola vez y reportar cobertura (nunca más fallos silenciosos)
        n_img = n_ref = n_depth = 0
        for item in self.data:
            mm = item.get("multimodal") or {}
            item["_img"] = self._resolver(mm.get("image"))
            item["_depth"] = self._resolver(mm.get("metric_depth")) if usar_profundidad else None
            item["_cam"] = self._resolver(mm.get("camera")) if usar_camara else None
            n_ref += bool(mm.get("image"))
            n_img += bool(item["_img"])
            n_depth += bool(item["_depth"])
        self.n_con_imagen = n_img
        print(f"[DATA] {os.path.basename(jsonl_path)}: {len(self.data)} ejemplos | "
              f"con imagen RGB encontrada: {n_img}/{n_ref} referenciadas"
              + (f" | profundidad: {n_depth}" if usar_profundidad else ""))

    def _resolver(self, rel):
        if not rel:
            return None
        for cand in (os.path.join(self.assets_dir, rel), rel):
            if os.path.isfile(cand):
                return cand
        return None

    def __len__(self):
        return len(self.data)

    def _cargar_profundidad(self, path):
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
        if item.get("_depth"):
            res = self._cargar_profundidad(item["_depth"])
            if res is not None:
                dimg, lo, hi = res
                bloques.append((f"Mapa de profundidad métrica (claro = cerca; rango {lo:.1f}–{hi:.1f} m):", dimg))
            else:
                self._n_depth_mala = getattr(self, "_n_depth_mala", 0) + 1
                if self._n_depth_mala <= 5:
                    print(f"[WARN] {item.get('id')}: EXR de profundidad inválido (¿assets viejos?), se omite")
        camera_info = texto_camara(item["_cam"]) if item.get("_cam") else ""

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name_or_path", type=str, default="Qwen/Qwen2.5-VL-7B-Instruct")
    parser.add_argument("--train_file", type=str, default=os.path.join(PROJECT_DIR, "TRAINING/data/train_multimodal.jsonl"))
    parser.add_argument("--val_file", type=str, default=os.path.join(PROJECT_DIR, "TRAINING/data/validation_multimodal.jsonl"))
    parser.add_argument("--output_dir", type=str, default="./checkpoints")
    parser.add_argument("--batch_size", type=int, default=1, help="Usa 1 para L4 (24GB). Usa 2 para 4090/A6000. Usa 4 para A100 (80GB).")
    parser.add_argument("--push_to_hub", action="store_true", help="Subir el adaptador LoRA a Hugging Face al terminar")
    parser.add_argument("--hub_model_id", type=str, default=None, help="Ej: tu_usuario/qwen2.5-vl-aec-lora")
    parser.add_argument("--max_length", type=int, default=6144, help="Tokens máximos por ejemplo (imagen+texto+código)")
    parser.add_argument("--assets_dir", type=str, default=DEFAULT_ASSETS_DIR,
                        help="Carpeta que contiene out_assets/ (rutas del JSONL son relativas a ella)")
    parser.add_argument("--descargar_assets", action="store_true",
                        help=f"Descargar renders desde HF ({HF_ASSETS_REPO}) a --assets_dir antes de entrenar")
    parser.add_argument("--usar_profundidad", action=argparse.BooleanOptionalAction, default=True,
                        help="Incluir mapa de profundidad métrica EXR como 2ª imagen (--no-usar_profundidad para desactivar)")
    parser.add_argument("--usar_camara", action=argparse.BooleanOptionalAction, default=True,
                        help="Incluir datos de cámara como texto (--no-usar_camara para desactivar)")
    parser.add_argument("--min_pct_imagenes", type=float, default=0.7,
                        help="Aborta si menos de esta fracción de ejemplos tiene imagen (evita entrenar solo-texto sin querer). 0 = desactivar")
    parser.add_argument("--max_pixels", type=int, default=768 * 768, help="Resolución máxima por imagen (controla tokens visuales)")
    parser.add_argument("--num_epochs", type=float, default=2)
    parser.add_argument("--max_steps", type=int, default=-1, help="Para pruebas rápidas (smoke test)")
    parser.add_argument("--report_to", type=str, default="wandb", help="wandb | none")
    parser.add_argument("--lora_r", type=int, default=64, help="Rango LoRA (alpha = 2*r)")
    parser.add_argument("--save_steps", type=int, default=0,
                        help="Si >0: evalúa y guarda checkpoint cada N pasos (en vez de por época), "
                             "para no perder progreso si se cae")
    parser.add_argument("--resume_from_checkpoint", type=str, default=None,
                        help="Ruta a checkpoint-XXX (o 'last' = el más reciente en output_dir)")
    args = parser.parse_args()

    if args.descargar_assets:
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
    train_dataset = QwenVLDataset(args.train_file, processor, **ds_kw)
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

    trainer = Trainer(
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
