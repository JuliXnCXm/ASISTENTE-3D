import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el suelo
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))

# Crear la escalinata central
bpy.ops.mesh.primitive_cube_add(size=0.2, location=(0, -5, 0.1))
for i in range(10):
    bpy.context.view_layer.objects.active = bpy.data.objects[f"Cube"]
    bpy.ops.object.duplicate()
    bpy.context.view_layer.objects.active = bpy.data.objects[f"Cube.{i+1}"]
    bpy.context.view_layer.objects.active.location.x += 0.2 * i
    bpy.context.view_layer.objects.active.location.y -= 0.2 * (i + 1)

# Crear rampas de accesibilidad
for i in range(5):
    bpy.ops.mesh.primitive_cube_add(size=0.2, location=(i * 0.2 - 2.5, -5, -0.1))
    bpy.context.view_layer.objects.active = bpy.data.objects[f"Cube"]
    bpy.ops.object.duplicate()
    bpy.context.view_layer.objects.active = bpy.data.objects[f"Cube.{i+1}"]
    bpy.context.view_layer.objects.active.location.x += 0.2 * i
    bpy.context.view_layer.objects.active.location.y -= 0.2 * (i + 1)

# Crear jardineras de hormigón
bpy.ops.mesh.primitive_cube_add(size=2, location=(3, -5, 0))
bpy.context.view_layer.objects.active = bpy.data.objects["Cube"]
bpy.ops.object.duplicate()
bpy.context.view_layer.objects.active = bpy.data.objects["Cube.001"]
bpy.context.view_layer.objects.active.location.x -= 6

# Añadir iluminación de piso
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        bpy.ops.object.light_add(type='AREA', location=obj.location)
        light = bpy.context.object
        light.data.energy = 1000
        light.data.color = (1, 1, 1)

# Guardar el archivo si BLEND_OUT está definido
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])