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
muro.location = mathutils.Vector((longitud/2, alto/2, 0))
muro.rotation_euler = mathutils.Euler((0, 0, 0), 'XYZ')

# Crea un nuevo mesh para el muro
mesh = bpy.data.meshes.new("MuroMesh")
bpy.context.collection.objects.link(mesh)

# Define las coordenadas de los vértices del muro
vertices = [
    (-longitud/2, -alto/2, 0),
    (longitud/2, -alto/2, 0),
    (longitud/2, alto/2, 0),
    (-longitud/2, alto/2, 0)
]

# Define las coordenadas de los polígonos del muro
polys = [
    [(0, 1, 2), (0, 3, 2)],
    [(0, 4, 5), (0, 7, 6)]
]

# Define la normal y el sentido de recorrido para cada polígono
normals = [
    mathutils.Vector((0, 0, -1)),
    mathutils.Vector((0, 0, -1))
]
tris = [
    [(0, 1, 2), (0, 3, 2)],
    [(0, 4, 5), (0, 7, 6)]
]

# Crea el mesh del muro
mesh.from_pydata(vertices, [], polys)
mesh.update(calc_edges=True)

# Asigna la geometría al objeto del muro
muro.data = mesh

# Establece las dimensiones del muro en metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])