import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear la base de la cama
base = bpy.data.objects.new("Base", None)
base.dimensions = (1.6, 2.0, 0.3)  # Ancho x Largo x Altura en metros
bpy.context.collection.objects.link(base)

# Crear la estructura de madera de roble
for i in range(4):
    post = bpy.data.objects.new("Post", None)
    post.dimensions = (0.1, 2.0, 0.3)  # Ancho x Largo x Altura en metros
    post.location = (i * 0.4 - 0.6, 1.0, 0.15 + i * 0.3)
    bpy.context.collection.objects.link(post)

# Crear el colchón de textil blanco
colchon = bpy.data.objects.new("Colchon", None)
colchon.dimensions = (1.6, 2.0, 0.3)  # Ancho x Largo x Altura en metros
colchon.location = (0, 0, 0.35)
bpy.context.collection.objects.link(colchon)

# Asignar materiales
material_roble = bpy.data.materials.new(name="Robre")
material_roble.diffuse_color = (0.8, 0.4, 0.2)
for obj in bpy.context.collection.objects:
    if "Post" in obj.name:
        obj.data.materials.append(material_roble)

material_textil = bpy.data.materials.new(name="Textil")
material_textil.diffuse_color = (1, 1, 1)
colchon.data.materials.append(material_textil)

# Guardar el archivo si BLEND_OUT está definido
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])