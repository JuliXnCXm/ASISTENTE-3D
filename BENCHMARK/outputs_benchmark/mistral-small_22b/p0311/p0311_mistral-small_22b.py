import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el marco de la cama
frame = bpy.data.objects.new("Frame", None)
bpy.context.collection.objects.link(frame)

# Dimensiones del marco (en metros)
length = 2.0
width = 1.6
height = 0.5

# Crear los bordes del marco
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, height / 2))
frame_top = bpy.context.object
frame_top.scale = (length / 2, width / 2, height / 2)

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -height / 2))
frame_bottom = bpy.context.object
frame_bottom.scale = (length / 2, width / 2, height / 2)

# Crear las patas del marco
for x in [-width / 2, width / 2]:
    for z in [-length / 2, length / 2]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=height, location=(x, 0, z))
        leg = bpy.context.object
        frame.objects.link(leg)

# Crear el colchón
mattress = bpy.data.objects.new("Mattress", None)
bpy.context.collection.objects.link(mattress)

# Dimensiones del colchón (en metros)
mattress_length = 2.0
mattress_width = 1.5
mattress_height = 0.3

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, mattress_height / 2))
mattress_top = bpy.context.object
mattress_top.scale = (mattress_length / 2, mattress_width / 2, mattress_height / 2)

# Asignar materiales
materials = bpy.data.materials
wood_material = materials.new(name="Wood")
wood_material.diffuse_color = (0.8, 0.4, 0.1, 1)

white_material = materials.new(name="White")
white_material.diffuse_color = (1, 1, 1, 1)

frame.data.materials.append(wood_material)
mattress.data.materials.append(white_material)

# Guardar el archivo si BLEND_OUT está definido
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])