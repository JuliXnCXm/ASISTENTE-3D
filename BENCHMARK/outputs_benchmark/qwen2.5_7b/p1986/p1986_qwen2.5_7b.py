import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el piso
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, -0.2))
floor = bpy.context.object
floor.scale = (5, 5, 1)

# Crear la isla central
island_size = 3
bpy.ops.mesh.primitive_cube_add(size=island_size, location=(-1.5, 0, 0))
island = bpy.context.object
island.scale = (island_size, island_size, 0.1)

# Crear los gabinetes
cabinet_length = 2.5
cabinet_height = 0.8
cabinet_depth = 0.4

bpy.ops.mesh.primitive_cube_add(size=cabinet_depth, location=(-3, -1.25, cabinet_height / 2))
left_cabinet = bpy.context.object
left_cabinet.scale = (cabinet_length, cabinet_depth, cabinet_height)

bpy.ops.mesh.primitive_cube_add(size=cabinet_depth, location=(3, -1.25, cabinet_height / 2))
right_cabinet = bpy.context.object
right_cabinet.scale = (cabinet_length, cabinet_depth, cabinet_height)

# Crear la encimera de cuarzo
bpy.ops.mesh.primitive_plane_add(size=7, location=(-0.5, -1.25, 0))
quartz_counter = bpy.context.object
quartz_counter.scale = (7, 3, 0.1)

# Crear la campana extractora
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2))
hood = bpy.context.object
hood.scale = (2, 2, 1)

# Guardar el archivo .blend si existe BLEND_OUT
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)