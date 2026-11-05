import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
num_escalones = 5
ancho_total = 1.0
huella = 0.3
contrahuella = 0.18
ancho_escalon = huella / num_escalones

# --- Bucle para crear los escalones ---
for i in range(num_escalones):
    # Calcular posición X de cada escalón
    pos_x = -ancho_total / 2 + huella * (i + 1) / 2
    
    # Crear el escalón actual
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, contrahuella * (i + 1) / 2),
        scale=(huella, ancho_escalon, contrahuella)
    )
    escalon = bpy.context.active_object
    escalon.name = f"Escalon_{i+1}"