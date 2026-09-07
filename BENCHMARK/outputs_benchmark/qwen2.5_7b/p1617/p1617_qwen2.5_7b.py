import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el terreno plano de césped
terreno = bpy.data.meshes.new(name="Terreno")
obj = bpy.data.objects.new("Jardin", terreno)
bpy.context.collection.objects.link(obj)

# Definir la geometría del terreno (20x30 metros)
verts = [
    (-10, -15, 0),
    (10, -15, 0),
    (10, 15, 0),
    (-10, 15, 0)
]

edges = []
faces = [(0, 1, 2, 3)]

# Crear la geometría
terreno.from_pydata(verts, edges, faces)
terreno.update()

# Ajustar el material para simular césped
material = bpy.data.materials.new(name="Cesped")
material.use_nodes = True
bsdf = material.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.3, 0.75, 0.1, 1)
bsdf.inputs['Roughness'].default_value = 0.8

obj.data.materials.append(material)

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if "BLEND_OUT" in bpy.context.scene:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.context.scene["BLEND_OUT"])