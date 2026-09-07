import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el terreno plano de césped
terreno = bpy.data.meshes.new(name="Césped")
obj = bpy.data.objects.new("Terreno", terreno)
bpy.context.collection.objects.link(obj)

# Definir la geometría del terreno
verts = [
    (-10, -7.5, 0),
    (10, -7.5, 0),
    (10, 7.5, 0),
    (-10, 7.5, 0)
]

edges = []
faces = [(0, 1, 2, 3)]

# Crear la geometría
terreno.from_pydata(verts, edges, faces)
terreno.update()

# Asignar un material verde al terreno
material = bpy.data.materials.new(name="Césped Material")
material.diffuse_color = (0.451, 0.627, 0.184, 1)  # Color de césped
obj.data.materials.append(material)

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if "BLEND_OUT" in bpy.context.scene:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.context.scene["BLEND_OUT"])