import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el suelo
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 0))

# Crear las columnas
column_height = 2.5
for i in range(4):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=column_height, location=(i * 1 - 1.5, 0, 0))

# Crear el techo
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, column_height))

# Guardar el archivo si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])