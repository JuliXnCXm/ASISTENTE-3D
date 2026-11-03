#!/usr/bin/env python3
"""
upload_assets_to_hub.py
Sube todos los renders, modelos .blend y EXR al repositorio de Hugging Face.
Esto permite que el dataset sea 100% portable y visible para los asesores.
"""

import os
import argparse
from pathlib import Path
try:
    from huggingface_hub import HfApi, login
except ImportError:
    print("Instalando librerías...")
    os.system("pip install huggingface_hub")
    from huggingface_hub import HfApi, login

ROOT = Path(__file__).resolve().parent.parent.parent
DATASET_DIR = ROOT / "ASISTENTE-3D" / "DATASET"

def main():
    parser = argparse.ArgumentParser(description="Subir Assets a Hugging Face")
    parser.add_argument("--repo-id", type=str, required=True)
    parser.add_argument("--token", type=str, required=True)
    args = parser.parse_args()

    # Iniciar sesión
    login(token=args.token)
    api = HfApi()

    print(f"🚀 Subiendo Assets Visuales a: {args.repo_id}")

    # Subir la carpeta de Creación (out_assets)
    out_assets_path = DATASET_DIR / "out_assets"
    if out_assets_path.exists():
        print("Subiendo out_assets (Creación)... Esto tomará un tiempo debido al peso de los .blend y .exr.")
        api.upload_folder(
            folder_path=str(out_assets_path),
            repo_id=args.repo_id,
            repo_type="dataset",
            path_in_repo="out_assets"
        )
        print("✅ out_assets subido.")

    # Subir la carpeta de Edición (out_assets_edit)
    out_assets_edit_path = DATASET_DIR / "out_assets_edit"
    if out_assets_edit_path.exists():
        print("Subiendo out_assets_edit (Edición)...")
        api.upload_folder(
            folder_path=str(out_assets_edit_path),
            repo_id=args.repo_id,
            repo_type="dataset",
            path_in_repo="out_assets_edit"
        )
        print("✅ out_assets_edit subido.")

    print("\n🎉 ¡Todos los artefactos 3D y renders están ahora en la nube de Hugging Face!")

if __name__ == "__main__":
    main()
