import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear las columnas
for i in range(4):
    x = -3 + 1.5 * (i % 2) + 0.75 * (i // 2)
    y = 1.5 - 1.5 * (i < 2)
    bpy.ops.mesh.primitive_cube_add(size=0.2, location=(x, y, 0))
    bpy.context.object.scale = (0.2, 0.2, 2.5)

# Crear las vigas horizontales
bpy.ops.mesh.primitive_cube_add(size=0.1, location=(-3, -1.5, 2.4))
bpy.ops.mesh.primitive_cube_add(size=0.1, location=(3, -1.5, 2.4))
bpy.ops.mesh.primitive_cube_add(size=0.1, location=(-3, 1.5, 2.4))
bpy.ops.mesh.primitive_cube_add(size=0.1, location=(3, 1.5, 2.4))

# Crear las vigas verticales
for i in range(4):
    x = -3 + 0.75 * (i % 2)
    y = 1.5 - 0.75 * (i < 2)
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(x, y, 2.4))

# Crear el techo plano
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, 0, 2.4))