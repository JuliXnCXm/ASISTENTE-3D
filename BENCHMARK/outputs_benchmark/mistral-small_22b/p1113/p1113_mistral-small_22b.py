import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el suelo
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 0))
floor = bpy.context.object

# Crear las paredes
wall_height = 3.5
for i in range(-2, 3):
    for j in range(-1, 2):
        if abs(i) == 2 or abs(j) == 1:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(i, j, wall_height / 2))
            wall = bpy.context.object
            wall.scale.x = 4
            wall.scale.y = wall_height
            wall.data.materials.append(bpy.data.materials.new(name="Gris"))
            wall.data.materials[0].diffuse_color = (0.5, 0.5, 0.5)

# Crear la cama doble
bed_length = 2
bed_width = 1.4
bed_height = 0.5
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -1.75, wall_height / 2))
bed = bpy.context.object
bed.scale.x = bed_length
bed.scale.y = bed_width
bed.scale.z = bed_height
bed.data.materials.append(bpy.data.materials.new(name="Madera"))
bed.data.materials[0].diffuse_color = (0.8, 0.6, 0.3)

# Guardar el archivo si BLEND_OUT está definido
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])