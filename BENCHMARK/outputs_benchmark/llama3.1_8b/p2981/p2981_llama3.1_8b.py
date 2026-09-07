import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del bolardo
alto = 0.9
diametro = 0.3

# Crea un nuevo objeto cilíndrico en el origen
bolardo = bpy.data.objects.new("Bolardo", bpy.data.meshes.new("Bolardo"))

# Establece la posición y orientación del bolardo
bolardo.location = mathutils.Vector((0, 0, 0))
bolardo.rotation_euler = mathutils.Euler((0, 0, 0))

# Crea el mesh cilíndrico
verts = [
    (-diametro/2, -diametro/2, 0),
    (diametro/2, -diametro/2, 0),
    (diametro/2, diametro/2, 0),
    (-diametro/2, diametro/2, 0)
]
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0)
]

faces = []
for i in range(4):
    faces.append((i, (i+1) % 4))

mesh = bpy.data.meshes.new("Bolardo")
mesh.from_pydata(verts, edges, faces)
mesh.update(calc_edges=True)

bolardo.data = mesh

# Agrega el objeto a la escena
bpy.context.collection.objects.link(bolardo)

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])