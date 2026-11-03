#!/usr/bin/env python3
"""
push_to_hub.py
Sube el dataset estructurado (Train, Validation, Test) a Hugging Face Hub.
Permite ser utilizado para el Fine-Tuning posterior en máquinas cloud.
"""

import os
import argparse
from pathlib import Path
try:
    from datasets import load_dataset
    from huggingface_hub import HfApi, login
except ImportError:
    print("Error: Instala las librerías necesarias ejecutando:")
    print("pip install datasets huggingface_hub")
    exit(1)

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT / "ASISTENTE-3D" / "TRAINING" / "data"

def main():
    parser = argparse.ArgumentParser(description="Subir dataset a Hugging Face")
    parser.add_argument("--repo-id", type=str, required=True, help="Nombre del repositorio (ej. usuario/aec-procedural-blender)")
    parser.add_argument("--token", type=str, help="Token de Hugging Face (si no se provee, se usará el login interactivo)")
    args = parser.parse_args()

    # Login
    if args.token:
        login(token=args.token)
    else:
        # Esto abrirá un prompt en la terminal para pegar el token
        print("Iniciando sesión en Hugging Face...")
        login()
        
    print(f"\n🚀 Subiendo el dataset a: https://huggingface.co/datasets/{args.repo_id}")
    
    # Archivos a subir
    data_files = {
        "train": str(DATA_DIR / "train.jsonl"),
        "validation": str(DATA_DIR / "validation.jsonl"),
        "test": str(DATA_DIR / "test.jsonl"),
    }
    
    # Verificar que existan
    for split, path in data_files.items():
        if not os.path.exists(path):
            print(f"❌ Error: No se encontró el archivo {path}")
            return

    print("Cargando archivos locales...")
    dataset = load_dataset("json", data_files=data_files)
    
    print("Subiendo al Hub...")
    # Sube el dataset estructurado de forma privada por defecto (puedes cambiarlo a True para público)
    dataset.push_to_hub(args.repo_id, private=False)
    
    print("\n✅ ¡Dataset subido exitosamente!")
    print(f"Ahora puedes cargarlo en tu servidor de entrenamiento con:")
    print(f"dataset = load_dataset('{args.repo_id}')")

if __name__ == "__main__":
    main()
