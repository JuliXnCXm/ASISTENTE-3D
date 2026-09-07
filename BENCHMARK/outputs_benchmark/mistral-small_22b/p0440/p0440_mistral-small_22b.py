import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el colchón
colchon = bpy.data.objects.new("Colchon", None)
colchon.location = (0, 0, 0.1)
bpy.ops.object.transform_apply(scale=False)
bpy.context.view_layer.objects.active = colchon
bpy.ops.mesh.primitive_cube_add(size=2)
colchon.data.vertices[0].co.z -= 1
colchon.data.vertices[1].co.z -= 1
colchon.data.vertices[2].co.z -= 1
colchon.data.vertices[3].co.z -= 1
colchon.data.vertices[4].co.z -= 1
colchon.data.vertices[5].co.z -= 1
colchon.data.vertices[6].co.z -= 1
colchon.data.vertices[7].co.z -= 1
bpy.context.view_layer.objects.active = None

# Crear la estructura de madera
madera = bpy.data.objects.new("Madera", None)
madera.location = (0, 0, -0.5)
bpy.ops.object.transform_apply(scale=False)
bpy.context.view_layer.objects.active = madera
bpy.ops.mesh.primitive_cube_add(size=2)
madera.data.vertices[0].co.z -= 1
madera.data.vertices[1].co.z -= 1
madera.data.vertices[2].co.z -= 1
madera.data.vertices[3].co.z -= 1
madera.data.vertices[4].co.z -= 1
madera.data.vertices[5].co.z -= 1
madera.data.vertices[6].co.z -= 1
madera.data.vertices[7].co.z -= 1
bpy.context.view_layer.objects.active = None

# Asignar materiales
material_colchon = bpy.data.materials.new(name="ColchonMaterial")
material_colchon.diffuse_color = (1, 1, 1)
colchon.data.materials.append(material_colchon)

material_madera = bpy.data.materials.new(name="MaderaMaterial")
material_madera.diffuse_color = (0.8, 0.4, 0.2)
madera.data.materials.append(material_madera)

# Guardar el archivo si BLEND_OUT está definido
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])