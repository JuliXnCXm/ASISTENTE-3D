import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del bolardo
altura = 0.9  # metros
diametro = 0.2  # metros

# Crea el cilindro en el origen de coordenadas
cylinder = bpy.data.objects.new("Bolardo", bpy.data.meshes.new("Cilindro"))

# Define las propiedades del cilindro
cylinder.location = (0, 0, altura / 2)
cylinder.scale = (diametro / 2, diametro / 2, altura)

# Crea el mesh del cilindro
verts = [
    (-diametro / 2, -diametro / 2, 0),
    (diametro / 2, -diametro / 2, 0),
    (diametro / 2, diametro / 2, 0),
    (-diametro / 2, diametro / 2, 0)
]
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (0, 4), (1, 5), (2, 6), (3, 7), (4, 5), (5, 6), (6, 7), (7, 4)
]
faces = [
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (0, 4, 7, 3),
    (1, 5, 6, 2),
    (0, 1, 5, 4),
    (1, 2, 6, 5),
    (2, 3, 7, 6),
    (3, 0, 4, 7)
]
cylinder.data.from_pydata(verts + verts, edges, faces)
cylinder.data.update()

# Agrega el objeto a la escena
bpy.context.collection.objects.link(cylinder)

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])