import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del muro
longitud = 10
alto = 2.5
espesor = 0.2

# Define las dimensiones de la apertura para el portón
ancho_porton = 3

# Crea un cubo para el muro
muro = bpy.data.objects.new("Muro", bpy.data.meshes.new("Muro"))

# Define los vértices del muro
vertices = [
    (-longitud/2, -alto/2, -espesor/2),
    (longitud/2, -alto/2, -espesor/2),
    (longitud/2, alto/2, -espesor/2),
    (-longitud/2, alto/2, -espesor/2),
    (-longitud/2 + ancho_porton/2, 0, -espesor/2)
]

# Define las caras del muro
caras = [
    (0, 1, 2, 3),  # Cara frontal
    (4, 5, 6, 7)   # Cara trasera
]

# Crea el polígono de la apertura para el portón
apertura = bpy.data.objects.new("Apertura", bpy.data.meshes.new("Apertura"))

# Define los vértices de la apertura
vertices_apertura = [
    (-longitud/2 + ancho_porton/2, 0, -espesor/2),
    (longitud/2 - ancho_porton/2, 0, -espesor/2),
    (longitud/2 - ancho_porton/2, alto/2, -espesor/2),
    (-longitud/2 + ancho_porton/2, alto/2, -espesor/2)
]

# Define las caras de la apertura
caras_apertura = [
    (0, 1, 2, 3)   # Cara frontal
]

# Crea el polígono del muro y la apertura
muro.data.from_pydata(vertices + vertices_apertura, [], caras + caras_apertura)
apertura.data.from_pydata(vertices_apertura, [], caras_apertura)

# Asigna los datos de la geometría al objeto
muro.data.update()
apertura.data.update()

# Agrega el muro y la apertura a la escena
bpy.context.collection.objects.link(muro)
bpy.context.collection.objects.link(apertura)

# Aplica la transformación para colocar el muro en su posición final
muro.location = (0, 0, -espesor/2)
apertura.location = (0, 0, -espesor/2)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])