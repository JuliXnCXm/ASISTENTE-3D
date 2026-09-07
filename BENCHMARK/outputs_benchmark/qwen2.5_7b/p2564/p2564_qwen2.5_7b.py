import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el piso
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, -0.15))
bpy.context.object.scale = (5, 4, 1)
bpy.ops.transform.resize(value=(5, 4, 2.7))

# Crear el techo
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 2.85))
bpy.context.object.scale = (5, 4, 1)
bpy.ops.transform.resize(value=(5, 4, 2.7))

# Crear las paredes
bpy.ops.mesh.primitive_cube_add(size=0.3, location=(-2.5, -2, 0))
bpy.context.object.scale = (5, 0.15, 2.7)
bpy.ops.transform.resize(value=(5, 0.15, 2.7))

bpy.ops.mesh.primitive_cube_add(size=0.3, location=(2.5, -2, 0))
bpy.context.object.scale = (5, 0.15, 2.7)
bpy.ops.transform.resize(value=(5, 0.15, 2.7))

bpy.ops.mesh.primitive_cube_add(size=0.3, location=(-2.5, 2, 0))
bpy.context.object.scale = (4, 0.15, 2.7)
bpy.ops.transform.resize(value=(4, 0.15, 2.7))

bpy.ops.mesh.primitive_cube_add(size=0.3, location=(2.5, 2, 0))
bpy.context.object.scale = (4, 0.15, 2.7)
bpy.ops.transform.resize(value=(4, 0.15, 2.7))

# Colocar una cama simple
bpy.ops.mesh.primitive_cube_add(size=1.5, location=(-1.5, -1, 0))
bpy.context.object.scale = (1.5, 0.3, 0.1)
bpy.ops.transform.resize(value=(1.5, 0.3, 2.7))

# Colocar una mesa de noche
bpy.ops.mesh.primitive_cube_add(size=0.8, location=(-1.5, -2.5, 0))
bpy.context.object.scale = (0.8, 0.4, 0.1)
bpy.ops.transform.resize(value=(0.8, 0.4, 2.7))

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if 'BLEND_OUT' in dir(bpy):
    bpy.ops.wm.save_as_mainfile(filepath=bpy.context.scene.BLEND_OUT)