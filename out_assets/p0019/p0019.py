import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_riel = 3.0
ancho_riel = 0.05
alto_riel = 0.05
num_focos = 4
diametro_foco = 0.08
largo_foco = 0.12
altura_techo = 2.8

# Crear el riel
loc_riel = (largo_riel / 2, 0, altura_techo - alto_riel / 2)
bpy.ops.mesh.primitive_cube_add(size=1, location=loc_riel)
riel = bpy.context.active_object
riel.name = "RielIluminacion"
riel.scale = (largo_riel, ancho_riel, alto_riel)

# Crear los focos
espaciado = largo_riel / (num_focos + 1)
for i in range(num_focos):
    x_pos = (i + 1) * espaciado
    loc_foco = (x_pos, 0, altura_techo - alto_riel - largo_foco / 2)
    
    bpy.ops.mesh.primitive_cylinder_add(
        radius=diametro_foco / 2,
        depth=largo_foco,
        location=loc_foco,
        rotation=(math.radians(45), 0, 0) # Rotación para orientarlo
    )
    foco = bpy.context.active_object
    foco.name = f"Foco_{i+1}"