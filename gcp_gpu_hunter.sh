#!/bin/bash
# ==============================================================================
# GCP GPU Hunter - Buscador de disponibilidad de NVIDIA A100 (40GB)
# ==============================================================================

PROJECT=$(gcloud config get-value project)
if [ -z "$PROJECT" ]; then
    echo "❌ No estás autenticado en Google Cloud o no tienes un proyecto configurado."
    echo "Ejecuta: gcloud auth login && gcloud config set project TU_PROYECTO"
    exit 1
fi

echo "🔍 Buscando disponibilidad de NVIDIA A100 (a2-highgpu-1g) en $PROJECT..."
echo "Esto tomará unos segundos mientras consulta a los centros de datos de Google."
echo "---------------------------------------------------------"

# Lista de zonas comunes donde suele haber A100
ZONES=("us-central1-a" "us-central1-b" "us-central1-c" "us-central1-f" \
       "us-east1-b" "us-east1-c" "us-east1-d" \
       "us-east4-a" "us-east4-b" "us-east4-c" \
       "us-west1-a" "us-west1-b" "us-west1-c" \
       "us-west4-a" "us-west4-b" \
       "europe-west4-a" "europe-west4-b" "europe-west4-c")

AVAILABLE_ZONES=()

for ZONE in "${ZONES[@]}"; do
    # Intenta simular la creación de la máquina (Dry Run) sin cobrar ni crearla
    OUTPUT=$(gcloud compute instances create test-a100-availability-$$ \
        --project="$PROJECT" \
        --zone="$ZONE" \
        --machine-type=a2-highgpu-1g \
        --maintenance-policy=TERMINATE \
        --image-family=common-cu121-debian-11 \
        --image-project=deeplearning-platform-release \
        --boot-disk-size=200GB \
        --dry-run 2>&1)

    if echo "$OUTPUT" | grep -q "currently unavailable"; then
        echo "❌ $ZONE: Agotadas (Unavailable)"
    elif echo "$OUTPUT" | grep -q "quota"; then
        echo "⚠️  $ZONE: No tienes cuota (Quota Exceeded)"
    elif echo "$OUTPUT" | grep -q "not found"; then
        echo "🚫 $ZONE: No existe este tipo de máquina aquí"
    elif echo "$OUTPUT" | grep -q "would be created"; then
        echo "✅ $ZONE: ¡A100 DISPONIBLE!"
        AVAILABLE_ZONES+=("$ZONE")
    else
        echo "❓ $ZONE: Estado desconocido ($OUTPUT)"
    fi
done

echo "---------------------------------------------------------"
if [ ${#AVAILABLE_ZONES[@]} -eq 0 ]; then
    echo "😭 Ninguna zona tiene A100 disponibles ahora mismo, o no tienes cuota."
    echo "💡 TIP: Intenta cambiar la máquina a L4 (g2-standard-4) en la consola."
else
    echo "🎉 ¡Buenas noticias! Ve a la consola de GCP y crea tu máquina en una de estas zonas:"
    for z in "${AVAILABLE_ZONES[@]}"; do
        echo " -> $z"
    done
fi
