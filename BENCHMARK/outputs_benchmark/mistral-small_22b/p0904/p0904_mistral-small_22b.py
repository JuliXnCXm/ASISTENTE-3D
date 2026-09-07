import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el colchón
colchon = bpy.data.objects.new("Colchon", None)
colchon.location = (0, 0, 0)
bpy.context.collection.objects.link(colchon)

# Añadir un material de textil blanco al colchón
material_blanco = bpy.data.materials.new(name="MaterialBlanco")
material_blanco.diffuse_color = (1, 1, 1, 1)
colchon.data.materials.append(material_blanco)

# Crear la estructura de madera de nogal
estructura = bpy.data.objects.new("Estructura", None)
estructura.location = (0, 0, 0)
bpy.context.collection.objects.link(estructura)

# Añadir un material de madera de nogal a la estructura
material_nogal = bpy.data.materials.new(name="MaterialNogal")
material_nogal.diffuse_color = (0.5, 0.35, 0.1, 1)
estructura.data.materials.append(material_nogal)

# Crear la geometría del colchón
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 1, 0))
colchon = bpy.context.object
colchon.scale = (1.6, 0.2, 2)

# Crear la geometría de la estructura
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, -1, 0))
estructura = bpy.context.object
estructura.scale = (1.6, 0.4, 2)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])