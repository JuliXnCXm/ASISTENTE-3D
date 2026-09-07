import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el suelo
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 0))
bpy.context.object.scale = (3, 1, 1)

# Crear los postes
for i in range(4):
    bpy.ops.mesh.primitive_cube_add(size=0.15, location=(i * 2 - 1, 0, 0))
    bpy.context.object.scale = (10, 10, 2.5)

# Crear las vigas horizontales
for i in range(4):
    bpy.ops.mesh.primitive_cube_add(size=0.15, location=(i * 2 - 1, 3, 0))
    bpy.context.object.scale = (4, 0.15, 0.15)

# Crear las vigas verticales
for i in range(4):
    for j in range(3):
        bpy.ops.mesh.primitive_cube_add(size=0.15, location=(i * 2 - 1, j * 1 + 0.75, 0))
        bpy.context.object.scale = (0.15, 2, 0.15)

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])