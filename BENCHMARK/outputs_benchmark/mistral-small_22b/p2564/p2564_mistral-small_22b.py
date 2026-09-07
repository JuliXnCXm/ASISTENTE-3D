import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la habitación
width = 5
depth = 4
height = 2.7
wall_thickness = 0.15

# Crear el suelo
bpy.ops.mesh.primitive_cube_add(size=1, location=(width/2 - wall_thickness/2, depth/2 - wall_thickness/2, height/2))
bpy.context.object.scale = (width, depth, 0.1)

# Crear el techo
bpy.ops.mesh.primitive_cube_add(size=1, location=(width/2 - wall_thickness/2, depth/2 - wall_thickness/2, height))
bpy.context.object.scale = (width, depth, 0.1)

# Crear las paredes
for i in range(4):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(wall_thickness/2 if i % 2 == 0 else width - wall_thickness/2, wall_thickness/2 if i < 2 else depth - wall_thickness/2, height/2))
    bpy.context.object.scale = (wall_thickness, height, 1)
    if i % 2 == 0:
        bpy.context.object.rotation_euler = (0, 1.5708, 0)
    else:
        bpy.context.object.rotation_euler = (0, -1.5708, 0)

# Crear la cama simple
bpy.ops.mesh.primitive_cube_add(size=1, location=(width/2 - wall_thickness/2 + 0.3, depth/2 - wall_thickness/2 + 0.5, height/2 - 0.8))
bpy.context.object.scale = (1.4, 0.6, 0.1)

# Crear la mesa de noche
bpy.ops.mesh.primitive_cube_add(size=1, location=(width/2 - wall_thickness/2 + 0.3, depth/2 - wall_thickness/2 + 0.5, height/2 - 0.8))
bpy.context.object.scale = (0.4, 0.4, 0.1)

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])