#!/bin/bash
# ============================================================================
# ORQUESTADOR DE PRODUCCIÓN - TESIS ASISTENTE 3D
# ============================================================================
# Este script levanta el ecosistema completo en modo "Monolito" en GCP.
# 1. vLLM (Inferencia) en el puerto 8000
# 2. FastAPI (Backend + LangGraph) en el puerto 8080
# Requiere tener 'tmux' instalado (sudo apt install tmux)
# ============================================================================

# 1. Matar procesos anteriores por si acaso
echo "Limpiando puertos y memoria..."
fuser -k 8000/tcp
fuser -k 8080/tcp
fuser -k /dev/nvidia0

# 2. Crear sesión de tmux para el LLM
echo "Levantando vLLM en segundo plano (tmux session: vllm_server)..."
tmux new-session -d -s vllm_server 'bash ASISTENTE-3D/LANZAR_VLLM_GCP.sh'

echo "Esperando 30 segundos para que vLLM cargue los pesos en la GPU..."
sleep 30

# 3. Crear sesión de tmux para el Backend
echo "Levantando Backend FastAPI en segundo plano (tmux session: backend_server)..."
tmux new-session -d -s backend_server 'cd asistente-3d-UI/asistente-3d-UI-back && source ../../venv_tesis/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8080'

echo "==========================================================================="
echo "¡SISTEMA EN LÍNEA!"
echo "---------------------------------------------------------------------------"
echo "El servidor de IA está en: http://localhost:8000"
echo "La API del Backend está en: http://<IP_PUBLICA_DE_ESTA_MAQUINA>:8080"
echo ""
echo "Para ver los logs de la IA usa:      tmux attach-session -t vllm_server"
echo "Para ver los logs del Backend usa:   tmux attach-session -t backend_server"
echo "(Para salir de los logs sin apagarlos presiona: Ctrl+B y luego la tecla D)"
echo "==========================================================================="
