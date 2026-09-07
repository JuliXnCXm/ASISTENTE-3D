import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea el dormitorio
floor = bpy.data.objects.new("Floor", None)
wall1 = bpy.data.objects.new("Wall1", None)
wall2 = bpy.data.objects.new("Wall2", None)
wall3 = bpy.data.objects.new("Wall3", None)
wall4 = bpy.data.objects.new("Wall4", None)
ceiling = bpy.data.objects.new("Ceiling", None)

bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
floor = bpy.context.object
floor.scale = (4, 3.5, 0.1)

bpy.ops.mesh.primitive_cube_add(location=(2, 0, 0))
wall1 = bpy.context.object
wall1.scale = (0.1, 3.5, 4)

bpy.ops.mesh.primitive_cube_add(location=(-2, 0, 0))
wall2 = bpy.context.object
wall2.scale = (0.1, 3.5, 4)

bpy.ops.mesh.primitive_cube_add(location=(0, 1.75, 0))
wall3 = bpy.context.object
wall3.scale = (4, 0.1, 3.5)

bpy.ops.mesh.primitive_cube_add(location=(0, -1.75, 0))
wall4 = bpy.context.object
wall4.scale = (4, 0.1, 3.5)

bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 4))
ceiling = bpy.context.object
ceiling.scale = (4, 3.5, 0.1)

# Pinta las paredes de gris
for obj in [wall1, wall2, wall3, wall4]:
    obj.data.materials.append(bpy.data.materials.new("GrayMaterial"))
    obj.data.materials[0].diffuse_color = (0.5, 0.5, 0.5)

# Crea la cama doble con estructura de madera
bed = bpy.data.objects.new("Bed", None)
bpy.ops.mesh.primitive_cube_add(location=(2, 1.75, -0.8))
bed = bpy.context.object
bed.scale = (2, 1, 0.4)

# Guarda el archivo si BLEND_OUT está definido
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])