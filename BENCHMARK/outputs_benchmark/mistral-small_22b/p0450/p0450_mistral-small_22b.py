import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el colchón
colchon = bpy.data.objects.new("Colchon", None)
colchon.location = (0, 0, 0.5)
bpy.ops.object.mode_set(mode='EDIT')
bpy.context.view_layer.objects.active = colchon
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
bpy.ops.transform.resize(value=(1, 2, 0.5))
bpy.context.view_layer.objects.active = None
bpy.ops.object.mode_set(mode='OBJECT')
colchon.data.materials.append(bpy.data.materials.new(name="Material"))
colchon.data.materials[0].diffuse_color = (1, 1, 1)

# Crear la estructura de madera
madera = bpy.data.objects.new("Madera", None)
madera.location = (0, 0, -0.5)
bpy.ops.object.mode_set(mode='EDIT')
bpy.context.view_layer.objects.active = madera
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
bpy.ops.transform.resize(value=(1, 2, 0.5))
bpy.context.view_layer.objects.active = None
bpy.ops.object.mode_set(mode='OBJECT')
madera.data.materials.append(bpy.data.materials.new(name="Material"))
madera.data.materials[0].diffuse_color = (0.5, 0.35, 0.1)

# Guardar el archivo si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])