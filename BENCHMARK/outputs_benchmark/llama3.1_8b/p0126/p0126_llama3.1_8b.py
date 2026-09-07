import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del muro
longitud = 4.0
alto = 2.5
espesor = 0.15

# Crea un nuevo objeto para el muro
muro = bpy.data.objects.new("Muro", None)
bpy.context.collection.objects.link(muro)

# Establece la posición del muro en los ejes X, Y y Z
muro.location = mathutils.Vector((longitud / 2, alto / 2, espesor / 2))

# Crea un nuevo mesh para el muro
mesh = bpy.data.meshes.new("MuroMesh")
bpy.context.collection.objects.link(mesh)

# Define los vértices del muro
vertices = [
    (-longitud/2, -alto/2, -espesor/2),
    ( longitud/2, -alto/2, -espesor/2),
    ( longitud/2,  alto/2, -espesor/2),
    (-longitud/2,  alto/2, -espesor/2),
    (-longitud/2, -alto/2,   espesor/2),
    ( longitud/2, -alto/2,   espesor/2),
    ( longitud/2,  alto/2,   espesor/2),
    (-longitud/2,  alto/2,   espesor/2)
]

# Define las caras del muro
faces = [
    (0, 1, 2, 3), # Cara superior
    (4, 5, 6, 7), # Cara inferior
    (0, 1, 5, 4), # Cara izquierda
    (1, 2, 6, 5), # Cara derecha
    (3, 2, 6, 7), # Cara trasera
    (4, 0, 3, 7)   # Cara delante
]

# Define los bordes del muro
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4)
]

# Crea el mesh del muro
mesh.from_pydata(vertices, edges, faces)
mesh.update(calc_edges=True)

# Asigna el mesh al objeto del muro
muro.data = mesh

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])