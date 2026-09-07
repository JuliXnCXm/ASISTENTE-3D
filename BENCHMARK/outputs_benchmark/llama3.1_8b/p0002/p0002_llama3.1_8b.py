import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del muro
longitud = 5
alto = 2.5
espesor = 0.15

# Crea un nuevo objeto para el muro
muro = bpy.data.objects.new("Muro", None)
bpy.context.collection.objects.link(muro)

# Establece la posición y orientación del muro
muro.location = mathutils.Vector((longitud / 2, alto / 2, espesor / 2))
muro.rotation_euler = (0, 0, 0)  # Rotación en el eje Z

# Crea un nuevo mesh para el muro
mesh = bpy.data.meshes.new("MuroMesh")
bpy.context.collection.objects.link(mesh)

# Define los vértices del muro
vertices = [
    (-longitud / 2, -alto / 2, -espesor / 2),
    (longitud / 2, -alto / 2, -espesor / 2),
    (longitud / 2, alto / 2, -espesor / 2),
    (-longitud / 2, alto / 2, -espesor / 2),
    (-longitud / 2, -alto / 2, espesor / 2),
    (longitud / 2, -alto / 2, espesor / 2),
    (longitud / 2, alto / 2, espesor / 2),
    (-longitud / 2, alto / 2, espesor / 2)
]

# Define las caras del muro
faces = [
    [0, 1, 2],
    [2, 3, 0],
    [4, 5, 6],
    [6, 7, 4]
]

# Define los bordes del muro
edges = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 0],
    [4, 5],
    [5, 6],
    [6, 7],
    [7, 4]
]

# Crea el mesh del muro
mesh.from_pydata(vertices, edges, faces)
mesh.update(calc_edges=True)

# Asigna la geometría al objeto del muro
muro.data = mesh

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])