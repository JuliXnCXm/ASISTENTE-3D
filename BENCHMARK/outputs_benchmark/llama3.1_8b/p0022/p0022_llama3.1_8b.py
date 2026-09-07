import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del muro divisorio
longitud = 5
alto = 2.8
espesor = 0.15

# Crea un nuevo objeto para el muro divisorio
muro = bpy.data.objects.new("MuroDivisorio", None)

# Establece la posición y orientación del muro divisorio
muro.location = mathutils.Vector((longitud/2, alto/2, 0))
muro.rotation_euler = (0, 0, 0)

# Crea un nuevo mesh para el muro divisorio
mesh = bpy.data.meshes.new("MuroDivisorioMesh")
verts = [
    (-espesor/2, -alto/2, 0),
    (longitud + espesor/2, -alto/2, 0),
    (longitud + espesor/2, alto/2, 0),
    (-espesor/2, alto/2, 0)
]
faces = [
    (0, 1, 2, 3)
]

mesh.from_pydata(verts, [], faces)
mesh.update(calc_edges=True)

# Asigna el mesh al objeto del muro divisorio
muro.data = mesh

# Agrega el objeto a la escena
bpy.context.collection.objects.link(muro)

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])