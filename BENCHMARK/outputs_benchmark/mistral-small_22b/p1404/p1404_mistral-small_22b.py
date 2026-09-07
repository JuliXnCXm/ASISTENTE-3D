import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea el muro de contención
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
wall = bpy.context.object
wall.scale = (10, 1.2, 0.3)  # 10 metros de largo y 1.2 metros de alto

# Crea la baranda metálica
bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=10, location=(0, 1.2, 0))
railing = bpy.context.object
railing.scale = (1, 1, 1)  # Ajusta el tamaño si es necesario

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])