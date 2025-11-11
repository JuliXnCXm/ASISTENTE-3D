import bpy
import math

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
altura_total = 3.0
ancho_escalera = 1.0
huella = 0.28
contrahuella = 0.18

# Cálculo del número de escalones
num_escalones = math.ceil(altura_total / contrahuella)
contrahuella_ajustada = altura_total / num_escalones

# Creación de los escalones en un bucle
for i in range(num_escalones):
    pos_x = (i + 0.5) * huella
    pos_y = ancho_escalera / 2
    pos_z = (i + 0.5) * contrahuella_ajustada
    
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, pos_y, pos_z - contrahuella_ajustada / 2),
        scale=(huella, ancho_escalera, contrahuella_ajustada)
    )
    escalon = bpy.context.active_object
    escalon.name = f"Escalon_{i+1:02d}"