import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el tramo de acera
acera = bpy.data.objects.new(name="Acera", object_data=None)
bpy.context.collection.objects.link(acera)
bpy.context.view_layer.objects.active = acera

bpy.ops.mesh.primitive_plane_add(size=2, location=(5, 0, -0.1))
bpy.ops.transform.resize(value=(10, 2, 1))

# Crear la baranda metálica
baranda = bpy.data.objects.new(name="Baranda", object_data=None)
bpy.context.collection.objects.link(baranda)
bpy.context.view_layer.objects.active = baranda

bpy.ops.mesh.primitive_cube_add(size=0.5, location=(5, 1, 0.2))
bpy.ops.transform.resize(value=(10, 0.1, 1))

# Añadir material a la baranda
material = bpy.data.materials.new(name="BarandaMaterial")
material.diffuse_color = (0.8, 0.6, 0.4, 1)
baranda.data.materials.append(material)

# Crear la calzada de asfalto
calzada = bpy.data.objects.new(name="Calzada", object_data=None)
bpy.context.collection.objects.link(calzada)
bpy.context.view_layer.objects.active = calzada

bpy.ops.mesh.primitive_plane_add(size=20, location=(-5, 0, -0.1))
bpy.ops.transform.resize(value=(20, 4, 1))

# Añadir material a la calzada
material_calzada = bpy.data.materials.new(name="CalzadaMaterial")
material_calzada.diffuse_color = (0.5, 0.5, 0.5, 1)
calzada.data.materials.append(material_calzada)

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)