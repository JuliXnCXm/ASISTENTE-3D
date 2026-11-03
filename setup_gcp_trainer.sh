#!/bin/bash
# ==============================================================================
# Setup rápido para máquinas en Google Cloud Platform (GCP)
# Optimizado para Deep Learning VM Images (Ubuntu 22.04 / Python 3.12)
# ==============================================================================

echo "🚀 Iniciando configuración de entorno GCP para Fine-Tuning de la Tesis..."

# 1. Actualizar el sistema e instalar dependencias base (OpenCV headless necesita libgl1)
sudo apt-get update -y
sudo apt-get install -y git wget bzip2 htop tmux python3-pip python3-venv libgl1-mesa-glx libglib2.0-0

# 2. Crear entorno virtual (Para no chocar con las librerías base del sistema M132)
echo "📦 Creando entorno virtual..."
python3 -m venv venv_tesis
source venv_tesis/bin/activate

# 3. Asegurar pip actualizado
echo "🔥 Preparando gestor de paquetes..."
pip install --upgrade pip

# 4. Instalar las dependencias exactas del proyecto (El PyTorch base ya viene con la imagen, aquí solo agregamos TRL, PEFT, etc.)
echo "📚 Instalando requerimientos de entrenamiento..."
cd ASISTENTE-3D || echo "Advertencia: Ejecuta este script desde la raíz del repositorio."
pip install -r TRAINING/requirements_training.txt

# 5. Iniciar sesión en Hugging Face
echo "🤗 Configurando Hugging Face..."
pip install -U "huggingface_hub[cli]"
echo "Por favor, pega tu token de Hugging Face (permisos WRITE) a continuación:"
huggingface-cli login

# 6. Iniciar sesión en Weights & Biases
echo "📈 Configurando Weights & Biases (wandb)..."
echo "(Presiona Ctrl+C si no quieres usar wandb, el entrenamiento seguirá funcionando sin él)"
wandb login

echo "export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True" >> venv_tesis/bin/activate

echo "=============================================================================="
echo "✅ Entorno listo."
echo "Para comenzar el entrenamiento, asegúrate de activar el entorno virtual con:"
echo "source venv_tesis/bin/activate"
echo "Y luego lanza el script en background usando nohup:"
echo "nohup python ASISTENTE-3D/TRAINING/train_qlora_multimodal.py --model_name_or_path \"Qwen/Qwen2.5-VL-7B-Instruct\" --batch_size 1 --push_to_hub --hub_model_id \"TU_USUARIO_DE_HF/qwen2.5-vl-aec-lora\" > entrenamiento.log 2>&1 &"
echo "=============================================================================="
