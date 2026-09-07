import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear losa de piso
bpy.ops.mesh.primitive_cube_add(size=1, location=(3, 2, -0.1))
floor = bpy.context.object
floor.scale = (6, 4, 0.2)