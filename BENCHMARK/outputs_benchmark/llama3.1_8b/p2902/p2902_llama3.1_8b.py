import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea un nuevo objeto cilíndrico
cylinder = bpy.data.objects.new("Cilindro", bpy.data.meshes.new("Cilindro"))

# Define las propiedades del cilindro
cylinder.location = (0, 0, 0)
cylinder.scale = (1, 1, 1)

# Crea el mesh del cilindro
verts = [
    (-0.15, 0, 0),
    (0.15, 0, 0),
    (0.15, 0.8, 0),
    (-0.15, 0.8, 0)
]
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0)
]
faces = [
    (0, 1, 2, 3)
]

mesh = bpy.data.meshes.new("Cilindro")
mesh.from_pydata(verts, edges, faces)
mesh.update()

# Asigna el mesh al objeto
cylinder.data = mesh

# Agrega el objeto a la escena
bpy.context.collection.objects.link(cylinder)

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])