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
bpy.context.collection.objects.link(muro)

# Define las coordenadas del vértice superior izquierdo del muro
x, y, z = -longitud/2, alto/2 + espesor/2, 0

# Crea los vértices del muro
vertices = [
    mathutils.Vector((x, y, z)),
    mathutils.Vector((x + longitud, y, z)),
    mathutils.Vector((x + longitud, -alto/2 + espesor/2, z)),
    mathutils.Vector((x, -alto/2 + espesor/2, z))
]

# Crea las caras del muro
faces = [
    (0, 1, 2, 3)
]

# Crea un nuevo mesh para el muro
muro_mesh = bpy.data.meshes.new("MuroMesh")
bpy.context.collection.objects.link(muro)

# Asigna los vértices y caras al mesh del muro
muro_mesh.from_pydata(vertices, [], faces)
muro_mesh.update(calc_edges=True)

# Aplica la transformación de escala para definir el tamaño del muro
muro.scale((longitud, alto + espesor, 1))

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])