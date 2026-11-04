#!/bin/bash
# ============================================================================
# SCRIPT DE LANZAMIENTO DEL SERVIDOR DE INFERENCIA VLLM (Monolito)
# ============================================================================
# Este script carga tu modelo base + el adaptador LoRA entrenado directamente
# en la memoria de la GPU y expone una API compatible con OpenAI en el
# puerto 8000 para que el Backend de LangGraph (UI) pueda consumirlo.
# ============================================================================

# 1. Asegúrate de tener el entorno virtual activado
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Activando entorno virtual..."
    source venv_tesis/bin/activate
fi

# 2. Instalar vLLM si no está instalado
pip install vllm 

# 3. Limpiar memoria de la GPU por si quedó basura del entrenamiento
echo "Limpiando VRAM..."
fuser -k /dev/nvidia0

# 4. Lanzar el servidor vLLM
# - Usamos Qwen2.5-VL-7B-Instruct como base.
# - Le inyectamos el LoRA que acabas de subir a Hugging Face (--enable-lora).
# - Limitamos la longitud de contexto a 8192 para no explotar la memoria (--max-model-len).
# - Servimos en el puerto 8000 para que el Backend de FastAPI se conecte.

echo "================================================================"
echo " INICIANDO SERVIDOR VLLM EN http://localhost:8000/v1"
echo " (Manten esta terminal abierta o usa screen/tmux)"
echo "================================================================"

python -m vllm.entrypoints.openai.api_server \
    --model "Qwen/Qwen2.5-VL-7B-Instruct" \
    --enable-lora \
    --lora-modules aec-lora="julianG99/qwen2.5-vl-aec-lora" \
    --max-model-len 8192 \
    --gpu-memory-utilization 0.95 \
    --port 8000

