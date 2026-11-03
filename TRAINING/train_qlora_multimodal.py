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
    DataCollatorForSeq2Seq
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

class QwenVLDataset(Dataset):
    """Dataset Custom para cargar el JSONL Multimodal."""
    def __init__(self, jsonl_path, processor):
        self.data = []
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                self.data.append(json.loads(line))
        self.processor = processor

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        messages = item["messages"]
        multimodal = item.get("multimodal", {})
        
        qwen_messages = []
        for msg in messages:
            if msg["role"] == "user":
                content = []
                # 1. Inyectar Imagen RGB normal
                if multimodal.get("image") and os.path.exists(multimodal["image"]):
                    content.append({"type": "text", "text": "Fotografía de referencia (RGB):"})
                    content.append({"type": "image", "image": multimodal["image"]})
                    
                # 2. Inyectar EXR (Profundidad Métrica) como segunda imagen
                if multimodal.get("metric_depth") and os.path.exists(multimodal["metric_depth"]):
                    content.append({"type": "text", "text": "Mapa de Profundidad de la escena (en metros reales):"})
                    content.append({"type": "image", "image": multimodal["metric_depth"]})
                    
                # 3. Leer inyectar los metadatos de cámara (JSON) como texto matemático
                camera_info = ""
                if multimodal.get("camera") and os.path.exists(multimodal["camera"]):
                    try:
                        with open(multimodal["camera"], "r") as cam_f:
                            cam_data = json.load(cam_f)
                            # Extraer datos vitales para razonamiento espacial
                            focal = cam_data.get("focal_length_mm", "N/A")
                            pos = [round(x, 2) for x in cam_data.get("cam_to_world", [[0,0,0,0]])[0][:3]] # Fallback simplificado
                            camera_info = f"\n[Datos Físicos de Cámara -> Focal: {focal}mm]"
                    except Exception:
                        pass
                    
                clean_text = msg["content"].replace("<image>\n", "").strip()
                content.append({"type": "text", "text": f"Instrucción del usuario: {clean_text}{camera_info}"})
                
                qwen_messages.append({"role": "user", "content": content})
            else:
                qwen_messages.append({"role": msg["role"], "content": [{"type": "text", "text": msg["content"]}]})
        
        # Procesar con el tokenizer y controlar estrictamente la resolución máxima de la imagen para salvar VRAM
        text_prompt = self.processor.apply_chat_template(qwen_messages, tokenize=False, add_generation_prompt=False)
        
        # Cargar las imágenes físicas en memoria
        image_inputs = []
        for msg in qwen_messages:
            for c in msg["content"]:
                if c["type"] == "image":
                    img_path = c["image"]
                    if img_path.endswith(".exr"):
                        # Leer EXR (32-bit floats) y normalizarlo
                        exr_data = cv2.imread(img_path, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
                        if exr_data is not None:
                            exr_min, exr_max = np.min(exr_data), np.max(exr_data)
                            if exr_max > exr_min:
                                norm_img = (exr_data - exr_min) / (exr_max - exr_min) * 255.0
                            else:
                                norm_img = exr_data * 0
                            img_pil = Image.fromarray(norm_img.astype(np.uint8)).convert("RGB")
                            image_inputs.append(img_pil)
                    else:
                        image_inputs.append(Image.open(img_path).convert("RGB"))
                    
        # Tokenizar (Text + Imagen)
        inputs = self.processor(
            text=[text_prompt],
            images=image_inputs if image_inputs else None,
            padding="max_length",
            truncation=True,
            max_length=4096, 
            return_tensors="pt"
        )
        
        # Remover la dimensión batch extra
        inputs = {k: v.squeeze(0) for k, v in inputs.items()}
        inputs["labels"] = inputs["input_ids"].clone() # El modelo auto-enmascara el padding en el Trainer
        
        return inputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name_or_path", type=str, default="Qwen/Qwen2.5-VL-7B-Instruct")
    parser.add_argument("--train_file", type=str, default="TRAINING/data/train_multimodal.jsonl")
    parser.add_argument("--val_file", type=str, default="TRAINING/data/validation_multimodal.jsonl")
    parser.add_argument("--output_dir", type=str, default="./checkpoints")
    parser.add_argument("--batch_size", type=int, default=1, help="Usa 1 para L4 (24GB). Usa 2 para 4090/A6000. Usa 4 para A100 (80GB).")
    parser.add_argument("--push_to_hub", action="store_true", help="Subir el adaptador LoRA a Hugging Face al terminar")
    parser.add_argument("--hub_model_id", type=str, default=None, help="Ej: tu_usuario/qwen2.5-vl-aec-lora")
    args = parser.parse_args()

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
    processor = AutoProcessor.from_pretrained(args.model_name_or_path)
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        args.model_name_or_path,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.bfloat16
    )
    model.config.use_cache = False
    model = prepare_model_for_kbit_training(model)

    # LoRA (Fine-Tuning Adaptativo)
    print("Configurando LoRA Multimodal...")
    # Solo entrenaremos las capas lineales del LLM (Dejamos congelado el Encoder Visual pre-entrenado de Qwen)
    peft_config = LoraConfig(
        r=64,
        lora_alpha=128,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"], 
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    # Datasets
    print("Cargando y procesando Datasets (Esto puede tomar tiempo)...")
    train_dataset = QwenVLDataset(args.train_file, processor)
    val_dataset = QwenVLDataset(args.val_file, processor)

    # Determinar si la GPU soporta BFloat16 (Ampere o superior como A100, L4, RTX 3090+)
    # Si es una T4 (Turing) o anterior, se fuerza a usar FP16 estándar.
    use_bf16 = torch.cuda.is_bf16_supported() if torch.cuda.is_available() else False
    use_fp16 = not use_bf16
    print(f"Hardware Compute Type: {'BFloat16' if use_bf16 else 'Float16 (T4/Antiguas)'}")

    # Trainer
    grad_acc = 16 // args.batch_size # Mantiene el batch efectivo total en 16
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=grad_acc,
        gradient_checkpointing=True,   # Salva muchísima VRAM
        optim="paged_adamw_32bit",
        learning_rate=2e-4,
        bf16=use_bf16,
        fp16=use_fp16,
        logging_steps=10,
        eval_strategy="epoch",
        save_strategy="epoch",
        remove_unused_columns=False, # Vital para los modelos Multimodales
        report_to="wandb"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=DataCollatorForSeq2Seq(processor.tokenizer, pad_to_multiple_of=8)
    )

    print("Iniciando Entrenamiento...")
    trainer.train()
    
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
