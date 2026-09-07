import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear losa de hormigón
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.75))
bpy.context.object.scale = (4, 3, 0.15)

# Crear postes verticales
for i in range(4):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(i % 2 * 2 - 1, i // 2 * 2 - 1, -2.5))
    bpy.context.object.scale = (0.15, 0.15, 2.5)

# Crear vigas horizontales
for i in range(4):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(i % 2 * 2 - 1, i // 2 * 2 - 1, 2.5))
    bpy.context.object.scale = (0.15, 0.15, 3)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])