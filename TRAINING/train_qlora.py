#!/usr/bin/env python3
"""
train_qlora.py
Script robusto para Fine-Tuning de modelos de lenguaje para código CAD.
Usa Hugging Face Transformers, PEFT (LoRA), y BitsAndBytes (4-bit QLoRA).
Optimizado para VRAM y registro en Weights & Biases (wandb).
"""

import os
import argparse
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM

def parse_args():
    parser = argparse.ArgumentParser(description="QLoRA Fine-Tuning para Modelo AEC")
    parser.add_argument("--model_name_or_path", type=str, required=True, help="Ej: Qwen/Qwen2.5-Coder-7B-Instruct")
    parser.add_argument("--train_file", type=str, default="data/train.jsonl")
    parser.add_argument("--val_file", type=str, default="data/validation.jsonl")
    parser.add_argument("--output_dir", type=str, default="./checkpoints")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=2)
    parser.add_argument("--gradient_accumulation_steps", type=int, default=8)
    parser.add_argument("--learning_rate", type=float, default=2e-4)
    parser.add_argument("--lora_r", type=int, default=64)
    parser.add_argument("--lora_alpha", type=int, default=128)
    parser.add_argument("--max_seq_length", type=int, default=4096)
    parser.add_argument("--wandb_project", type=str, default="tesis-aec-cad")
    return parser.parse_args()

def main():
    args = parse_args()

    # Configurar wandb
    os.environ["WANDB_PROJECT"] = args.wandb_project

    # Cargar Datasets
    print("Cargando datasets...")
    dataset = load_dataset("json", data_files={"train": args.train_file, "validation": args.val_file})

    # Cargar Tokenizer
    print("Cargando Tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right" # Para SFT, padding derecho es generalmente mejor

    # Función de formateo de mensajes a ChatML o formato nativo del modelo
    def format_prompts_func(example):
        output_texts = []
        for i in range(len(example['id'])):
            messages = example['messages'][i]
            # Usa el template de chat nativo del tokenizador (Ej: <|im_start|>user...<|im_end|>)
            text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
            output_texts.append(text)
        return output_texts

    # Cuantización a 4-bits (BitsAndBytes)
    print("Configurando Cuantización 4-bits...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    # Cargar Modelo
    print(f"Cargando Modelo {args.model_name_or_path}...")
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name_or_path,
        quantization_config=bnb_config,
        device_map="auto", # Reparte en las GPUs disponibles
        trust_remote_code=True
    )
    model.config.use_cache = False # Apagar para entrenamiento
    model = prepare_model_for_kbit_training(model)

    # Configuración LoRA
    print("Configurando LoRA...")
    peft_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"] # Targetea todas las lineales para mejor adaptación
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    # Argumentos de Entrenamiento
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        gradient_checkpointing=True, # Ahorra muchísima VRAM
        optim="paged_adamw_32bit",
        logging_steps=10,
        save_strategy="epoch",
        evaluation_strategy="epoch",
        learning_rate=args.learning_rate,
        bf16=True, # Recomendado en Ampere (A100/A10/RTX 3090+)
        max_grad_norm=1.0,
        warmup_ratio=0.03,
        lr_scheduler_type="cosine",
        report_to="wandb",
    )

    # Trainer (Usando TRL)
    print("Iniciando Trainer...")
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
        peft_config=peft_config,
        formatting_func=format_prompts_func,
        max_seq_length=args.max_seq_length,
        tokenizer=tokenizer,
        args=training_args,
    )

    # ¡A Entrenar!
    print("Comenzando el Fine-Tuning...")
    trainer.train()
    
    # Guardar modelo final
    trainer.model.save_pretrained(os.path.join(args.output_dir, "final_adapter"))
    tokenizer.save_pretrained(os.path.join(args.output_dir, "final_adapter"))
    print("Entrenamiento completado. Adapters guardados.")

if __name__ == "__main__":
    main()
