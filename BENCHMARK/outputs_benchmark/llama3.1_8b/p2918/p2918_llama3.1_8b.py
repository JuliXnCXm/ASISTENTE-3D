import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del muro
longitud = 10  # metros
alto = 2.5  # metros
espesor = 0.2  # metros (20 cm)
ancho_porton = 3  # metros

# Crea un plano para el muro
muro = bpy.data.objects.new("Muro", bpy.data.meshes.new("Muro"))

# Define las coordenadas del vértice superior izquierdo del muro
x, y, z = -longitud/2, alto + espesor, 0

# Crea los vértices del muro
vertices = [
    (x, y, 0),  # Vértice superior izquierdo
    (x, y, longitud),  # Vértice superior derecho
    (-longitud/2, -espesor, 0),  # Vértice inferior izquierdo
    (longitud/2, -espesor, 0)  # Vértice inferior derecho
]

# Crea los vértices del portón
porton_vertices = [
    (x + ancho_porton/2, y, 0),  # Vértice superior izquierdo del portón
    (x + ancho_porton/2, y, longitud - ancho_porton),  # Vértice superior derecho del portón
    (-longitud/2 + ancho_porton/2, -espesor, 0),  # Vértice inferior izquierdo del portón
    (longitud/2 - ancho_porton/2, -espesor, 0)  # Vértice inferior derecho del portón
]

# Crea las caras del muro y del portón
faces_muro = [
    [0, 1, 2], [0, 1, 3]  # Caras superiores e inferiores
]
faces_porton = [
    [4, 5, 6], [4, 5, 7]  # Caras superiores e inferiores del portón
]

# Crea las caras del muro y del portón
muro.data.polygons.new("Face").vertices = faces_muro[0]
muro.data.polygons.new("Face").vertices = faces_muro[1]
porton_data = bpy.data.meshes.new("Portón")
porton_data.polygons.new("Face").vertices = faces_porton[0]
porton_data.polygons.new("Face").vertices = faces_porton[1]

# Crea los polígonos del muro y del portón
muro.data.from_pydata(vertices + vertices[:4], [], faces_muro)
porton_data.from_pydata(porton_vertices + porton_vertices[:4], [], faces_porton)

# Añade el muro y el portón a la escena
bpy.context.collection.objects.link(muro)
bpy.context.collection.objects.link(bpy.data.objects.new("Portón", porton_data))

# Escala el muro y el portón para que tengan las dimensiones correctas
muro.scale = (longitud, alto + espesor * 2, longitud)
porton_data.scale = (ancho_porton, alto + espesor * 2, ancho_porton)

# Guarda la escena si se especificó un archivo de salida
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])