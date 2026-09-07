import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del muro en metros
longitud = 5
alto = 2.7
espesor = 0.15

# Crea un nuevo objeto para el muro
muro = bpy.data.objects.new("Muro", None)

# Establece la posición y orientación del muro
muro.location = mathutils.Vector((0, 0, 0))
muro.rotation_euler = mathutils.Euler((0, 0, 0), 'XYZ')

# Crea un nuevo mesh para el muro
mesh_muro = bpy.data.meshes.new("Mesh_Muro")

# Define las coordenadas de los vértices del muro
vertices = [
    (-longitud/2, -alto/2, -espesor/2),
    (longitud/2, -alto/2, -espesor/2),
    (longitud/2, alto/2, -espesor/2),
    (-longitud/2, alto/2, -espesor/2),
    (-longitud/2, -alto/2, espesor/2),
    (longitud/2, -alto/2, espesor/2),
    (longitud/2, alto/2, espesor/2),
    (-longitud/2, alto/2, espesor/2)
]

# Define las caras del muro
faces = [
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (0, 1, 5, 4),
    (1, 2, 6, 5),
    (2, 3, 7, 6),
    (3, 0, 4, 7)
]

# Define los polígonos del muro
polygons = [
    ((0, 1, 2, 3), 'QUADS'),
    ((4, 5, 6, 7), 'QUADS'),
    ((0, 1, 5, 4), 'QUADS'),
    ((1, 2, 6, 5), 'QUADS'),
    ((2, 3, 7, 6), 'QUADS'),
    ((3, 0, 4, 7), 'QUADS')
]

# Crea el mesh del muro
mesh_muro.from_pydata(vertices, [], faces)
mesh_muro.update(calc_edges=True)

# Asigna el mesh al objeto del muro
muro.data = mesh_muro

# Agrega el objeto del muro a la escena actual
bpy.context.collection.objects.link(muro)

# Si existe la variable de entorno BLEND_OUT, guarda la escena en ese archivo
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])