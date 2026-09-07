import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el suelo
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
floor = bpy.context.object
floor.name = "Floor"

# Crear la isla central
bpy.ops.mesh.primitive_cube_add(size=2, location=(4, 3, 0.1))
island = bpy.context.object
island.name = "Island"

# Crear gabinetes
for i in range(5):
    bpy.ops.mesh.primitive_cube_add(size=2, location=(i * 2 - 8, -3, 0.1))
    cabinet = bpy.context.object
    cabinet.name = f"Cabinet_{i}"

# Crear encimeras de cuarzo
bpy.ops.mesh.primitive_plane_add(size=2, location=(4, 3, 0.1))
countertop = bpy.context.object
countertop.name = "Countertop"

# Crear campana extractora suspendida del techo
bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=1, depth=0.5, location=(4, 6, 3))
hood = bpy.context.object
hood.name = "Hood"

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as(filepath=os.environ['BLEND_OUT'])