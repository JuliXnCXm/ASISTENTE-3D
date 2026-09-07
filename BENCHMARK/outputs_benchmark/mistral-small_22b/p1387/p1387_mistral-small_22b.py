import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear la pared
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 5, 0))
wall = bpy.context.object
wall.scale.x = 10
wall.scale.y = 6

# Crear la puerta
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 2.5, -0.5))
door = bpy.context.object
door.scale.x = 3
door.scale.y = 4

# Crear las ventanas
for i in range(-1, 2):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(i * 3.5, 2.5, -0.5))
    window = bpy.context.object
    window.scale.x = 1
    window.scale.y = 2

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])