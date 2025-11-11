import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

largo_riel = 3.0
altura_techo = 2.8
num_focos = 3

# Crear Riel
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, altura_techo),
    scale=(largo_riel, 0.05, 0.025)
)
bpy.context.active_object.name = 'Riel'

# Crear Focos
distancia_entre_focos = largo_riel / (num_focos + 1)
for i in range(num_focos):
    x_pos = -largo_riel / 2 + distancia_entre_focos * (i + 1)
    
    # Conector
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.03, 
        depth=0.08, 
        location=(x_pos, 0, altura_techo - 0.05),
        rotation=(0, 0, 0)
    )
    bpy.context.active_object.name = f'ConectorFoco_{i+1}'
    
    # Cuerpo del foco
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.05, 
        depth=0.15, 
        location=(x_pos, 0, altura_techo - 0.125),
        rotation=(0, math.radians(30), 0)
    )
    bpy.context.active_object.name = f'CuerpoFoco_{i+1}'