import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones en metros
width = 4.0
length = 3.0
height = 2.5

# Crear postes cuadrados de 15x15 cm
post_size = 0.15 / 2  # Convertir a metros

# Crear los postes
for x in [-width/2, width/2]:
    for z in [-length/2, length/2]:
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(x, 0, z))
        cube = bpy.context.object
        cube.scale = (post_size, post_size, height)

# Crear la estructura de la pérgola
bpy.ops.mesh.primitive_plane_add(size=length, enter_editmode=False, align='WORLD', location=(0, width/2, 0))
plane1 = bpy.context.object

bpy.ops.mesh.primitive_plane_add(size=width, enter_editmode=False, align='WORLD', location=(-length/4, 0, height))
plane2 = bpy.context.object
plane2.rotation_euler[2] = 3.14159 / 2  # Rotar 90 grados alrededor del eje Y

bpy.ops.mesh.primitive_plane_add(size=width, enter_editmode=False, align='WORLD', location=(length/4, 0, height))
plane3 = bpy.context.object
plane3.rotation_euler[2] = -3.14159 / 2  # Rotar -90 grados alrededor del eje Y

# Alinear los planos con los postes
for plane in [plane1, plane2, plane3]:
    for x in [-width/2, width/2]:
        bpy.ops.object.select_all(action='DESELECT')
        plane.select_set(True)
        bpy.context.view_layer.objects.active = plane
        bpy.ops.transform.translate(value=(x, 0, 0), constraint_axis=(True, False, False))

# Unir todos los objetos en una sola mesh
bpy.ops.object.select_all(action='DESELECT')
for obj in [cube for cube in bpy.data.objects if "Cube" in cube.name] + [plane1, plane2, plane3]:
    obj.select_set(True)
bpy.context.view_layer.objects.active = plane1
bpy.ops.object.join()

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if 'BLEND_OUT' in bpy.context.scene:
    blend_out_path = bpy.context.scene['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)