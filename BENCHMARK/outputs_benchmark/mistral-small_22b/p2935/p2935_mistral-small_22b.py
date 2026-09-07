import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear losa de hormigón
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.75))
concrete_slab = bpy.context.object
concrete_slab.scale = (4, 3, 0.15)

# Crear postes de madera
for i in range(4):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(i * 2 - 2, 0, 0))
    post = bpy.context.object
    post.scale = (0.15, 0.15, 2.5)

# Crear vigas horizontales
for i in range(4):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(i * 2 - 2, 0, 2.5))
    beam = bpy.context.object
    beam.scale = (4, 3, 0.15)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])