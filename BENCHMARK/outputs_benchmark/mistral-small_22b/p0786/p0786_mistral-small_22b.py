import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el marco de la cama
frame = bpy.data.objects.new("Frame", None)
bpy.context.collection.objects.link(frame)
frame.location = (0, 0, 0)

# Crear los lados largos del marco
for i in range(-1, 2):
    bpy.ops.mesh.primitive_cube_add(size=2, location=(i * 1.6 / 2, -1, 0))
    cube = bpy.context.object
    cube.name = "LongSide" + str(abs(i) + 1)
    frame.objects.link(cube)

# Crear los lados cortos del marco
for i in range(-1, 2):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, i * 2 / 2, -1))
    cube = bpy.context.object
    cube.name = "ShortSide" + str(abs(i) + 1)
    frame.objects.link(cube)

# Crear las patas del marco
for i in range(-1, 2):
    for j in range(-1, 2):
        bpy.ops.mesh.primitive_cube_add(size=0.1, location=(i * 1.6 / 2, j * 2 / 2, -2))
        cube = bpy.context.object
        cube.name = "Leg" + str(abs(i) + 1) + str(abs(j) + 1)
        frame.objects.link(cube)

# Crear el colchón
bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, -0.5))
colchon = bpy.context.object
colchon.name = "Colchon"
frame.objects.link(colchon)

# Aplicar materiales
materials = bpy.data.materials
wood_material = materials.new(name="WoodMaterial")
wood_material.diffuse_color = (0.5, 0.3, 0.2)  # Color de nogal

textile_material = materials.new(name="TextileMaterial")
textile_material.diffuse_color = (1, 1, 1)  # Color blanco

for obj in frame.objects:
    if "LongSide" in obj.name or "ShortSide" in obj.name or "Leg" in obj.name:
        obj.data.materials.append(wood_material)

colchon.data.materials.append(textile_material)

# Guardar el archivo si BLEND_OUT está definido
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])