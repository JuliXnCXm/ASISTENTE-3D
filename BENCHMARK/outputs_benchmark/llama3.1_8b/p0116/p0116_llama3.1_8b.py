import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del muro en metros
longitud = 5
altura = 2.7
espesor = 0.15

# Crea un nuevo objeto para el muro
muro = bpy.data.objects.new("Muro", None)
bpy.context.collection.objects.link(muro)

# Define las coordenadas del vértice superior izquierdo del muro
x, y, z = -longitud/2, altura/2 + espesor/2, 0

# Crea los vértices del muro
vertices = [
    mathutils.Vector((x, y, z)),
    mathutils.Vector((x + longitud, y, z)),
    mathutils.Vector((x + longitud, y - altura + espesor, z)),
    mathutils.Vector((x, y - altura + espesor, z))
]

# Crea las caras del muro
faces = [
    (0, 1, 2, 3)
]

# Crea el objeto de geometría para el muro
muro_data = bpy.data.meshes.new("Muro")
muro_data.from_pydata(vertices, [], faces)
muro_data.update(calc_edges=True)

# Asigna la geometría al objeto del muro
muro.data = muro_data

# Establece las dimensiones del objeto en metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in bpy.context.env:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.env['BLEND_OUT'])