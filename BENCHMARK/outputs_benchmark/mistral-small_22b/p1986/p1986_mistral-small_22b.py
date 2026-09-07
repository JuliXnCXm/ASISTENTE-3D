import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea el suelo
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
floor = bpy.context.object
floor.name = "Floor"

# Crea la isla central
bpy.ops.mesh.primitive_cube_add(size=2, location=(3, 3, 0.1))
island = bpy.context.object
island.name = "Island"

# Crea los gabinetes
for i in range(-4, 5):
    for j in range(-4, 5):
        if abs(i) != 4 or abs(j) != 4:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(i, j, 0.9))
            cabinet = bpy.context.object
            cabinet.name = "Cabinet"

# Crea las encimeras de cuarzo
bpy.ops.mesh.primitive_plane_add(size=8, location=(0, 3, 1.5))
countertop = bpy.context.object
countertop.name = "Countertop"

# Crea la campana extractora
bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.5, depth=1, location=(4, 4, 3))
hood = bpy.context.object
hood.name = "Hood"

# Guarda el archivo .blend si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])