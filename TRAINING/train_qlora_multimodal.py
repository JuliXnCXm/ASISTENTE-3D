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
from PIL import Image
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
        
        # Formato de Qwen-VL: Espera [{"role": "user", "content": [{"type": "image", "image": "path"}, {"type": "text", "text": "Crea..."}]}]
        qwen_messages = []
        for msg in messages:
            if msg["role"] == "user":
                content = []
                # Si hay imagen, la inyectamos en el mensaje del usuario
                if "image" in multimodal and os.path.exists(multimodal["image"]):
                    content.append({"type": "image", "image": multimodal["image"]})
                # El texto sin el tag crudo <image> (Qwen-VL lo maneja internamente con el dict)
                clean_text = msg["content"].replace("<image>\n", "").strip()
                content.append({"type": "text", "text": clean_text})
                
                qwen_messages.append({"role": "user", "content": content})
            else:
                qwen_messages.append({"role": msg["role"], "content": [{"type": "text", "text": msg["content"]}]})
        
        # Procesar con el tokenizer y el image processor de Qwen
        text_prompt = self.processor.apply_chat_template(qwen_messages, tokenize=False, add_generation_prompt=False)
        
        # Cargar las imágenes en memoria
        image_inputs = []
        for msg in qwen_messages:
            for c in msg["content"]:
                if c["type"] == "image":
                    image_inputs.append(Image.open(c["image"]).convert("RGB"))
                    
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
    parser.add_argument("--train_file", type=str, default="data/train_multimodal.jsonl")
    parser.add_argument("--val_file", type=str, default="data/validation_multimodal.jsonl")
    parser.add_argument("--output_dir", type=str, default="./checkpoints")
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

    # Trainer
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8, # Efectivo Batch = 16
        gradient_checkpointing=True,   # Salva muchísima VRAM
        optim="paged_adamw_32bit",
        learning_rate=2e-4,
        bf16=True,
        logging_steps=10,
        evaluation_strategy="epoch",
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
    print("Entrenamiento Multimodal Finalizado y Adapters Guardados.")

if __name__ == "__main__":
    main()
