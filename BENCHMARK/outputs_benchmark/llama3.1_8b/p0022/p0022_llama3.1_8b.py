import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del muro
longitud = 5
alto = 2.8
espesor = 0.15

# Crea un nuevo objeto para el muro
muro = bpy.data.objects.new("Muro", None)

# Establece la posición y orientación del muro
muro.location = (0, 0, 0)
muro.rotation_euler = (0, 0, 0)

# Crea un nuevo mesh para el muro
mesh = bpy.data.meshes.new("MuroMesh")
obj = bpy.data.objects.new("Muro", mesh)

# Define las coordenadas de los vértices del muro
vertices = [
    (-longitud/2, -alto/2, espesor/2),
    (longitud/2, -alto/2, espesor/2),
    (longitud/2, alto/2, espesor/2),
    (-longitud/2, alto/2, espesor/2)
]

# Define las coordenadas de los polígonos del muro
polys = [
    [(0, 1, 2), (0, 3, 2)],
    [(4, 5, 6), (4, 7, 6)]
]

# Crea el mesh y lo asigna al objeto
mesh.from_pydata(vertices, [], polys)
mesh.update(calc_edges=True)

# Agrega el objeto a la escena
bpy.context.collection.objects.link(obj)

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])