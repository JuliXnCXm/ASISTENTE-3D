#!/bin/bash
# ==============================================================================
# Reintenta encender una VM con GPU hasta que GCP tenga capacidad en la zona.
# (Error típico al reanudar: ZONE_RESOURCE_POOL_EXHAUSTED / "does not have enough
#  resources available"). No cobra nada mientras la VM no arranca.
#
# Uso:  ./ARRANCAR_VM_REINTENTOS.sh NOMBRE_VM [ZONA] [ESPERA_SEG] [MAX_INTENTOS]
#   ej: ./ARRANCAR_VM_REINTENTOS.sh tesis-a100
#   ej: ./ARRANCAR_VM_REINTENTOS.sh tesis-a100 us-central1-a 120 300
# ==============================================================================
VM="$1"
ZONA="$2"
ESPERA="${3:-120}"
MAX="${4:-500}"

if [ -z "$VM" ]; then
    echo "Uso: $0 NOMBRE_VM [ZONA] [ESPERA_SEG] [MAX_INTENTOS]"
    echo "VMs en el proyecto:"
    gcloud compute instances list --format="table(name,zone.basename(),machineType.basename(),status)"
    exit 1
fi

if [ -z "$ZONA" ]; then
    ZONA=$(gcloud compute instances list --filter="name=($VM)" --format="value(zone.basename())")
    [ -z "$ZONA" ] && { echo "❌ No encontré la VM '$VM'"; exit 1; }
fi
echo "🎯 VM: $VM | zona: $ZONA | reintento cada ${ESPERA}s (máx $MAX intentos)"

for ((i = 1; i <= MAX; i++)); do
    OUT=$(gcloud compute instances start "$VM" --zone="$ZONA" 2>&1)
    if [ $? -eq 0 ]; then
        IP=$(gcloud compute instances describe "$VM" --zone="$ZONA" \
             --format="value(networkInterfaces[0].accessConfigs[0].natIP)")
        echo "✅ [$(date +%H:%M:%S)] ¡VM encendida en el intento $i! IP externa: $IP"
        echo "   Conéctate con: gcloud compute ssh $VM --zone=$ZONA"
        command -v notify-send >/dev/null && notify-send "GPU conseguida" "$VM encendida ($ZONA)"
        printf '\a'
        exit 0
    fi
    if echo "$OUT" | grep -qiE "RESOURCE_POOL_EXHAUSTED|not have enough resources|currently unavailable|STOCKOUT"; then
        echo "⏳ [$(date +%H:%M:%S)] Intento $i: sin A100 libres en $ZONA. Reintento en ${ESPERA}s..."
    elif echo "$OUT" | grep -qi "quota"; then
        echo "⚠️  Error de CUOTA (no es falta de stock):"; echo "$OUT"; exit 2
    else
        echo "❓ [$(date +%H:%M:%S)] Intento $i, error inesperado:"; echo "$OUT"
    fi
    sleep "$ESPERA"
done
echo "😭 No se consiguió GPU tras $MAX intentos."
exit 1
