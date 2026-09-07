import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del muro y la puerta
longitud_muro = 10
alto_muro = 2.2
ancho_puerta = 1

# Crea el muro
muro = bpy.data.objects.new("Muro", bpy.data.meshes.new("Muro"))
muro.location = mathutils.Vector((0, 0, 0))
muro.scale = (longitud_muro, alto_muro, 0.01)

# Crea la geometría del muro
verts = [
    (-longitud_muro/2, -alto_muro/2, 0),
    (longitud_muro/2, -alto_muro/2, 0),
    (longuidad_muro/2, alto_muro/2, 0),
    (-longitud_muro/2, alto_muro/2, 0)
]
faces = [
    (0, 1, 2, 3)
]

muro.data.from_pydata(verts, [], faces)
bpy.context.collection.objects.link(muro)

# Crea la puerta
puerta = bpy.data.objects.new("Puerta", bpy.data.meshes.new("Puerta"))
puerta.location = mathutils.Vector((0, 0, 0))
puerta.scale = (ancho_puerta, alto_muro, 0.01)

# Crea la geometría de la puerta
verts = [
    (-ancho_puerta/2, -alto_muro/2, 0),
    (ancho_puerta/2, -alto_muro/2, 0),
    (ancho_puerta/2, alto_muro/2, 0),
    (-ancho_puerta/2, alto_muro/2, 0)
]
faces = [
    (0, 1, 2, 3)
]

puerta.data.from_pydata(verts, [], faces)
bpy.context.collection.objects.link(puerta)

# Posiciona la puerta en el centro del muro
puerta.location.x += longitud_muro/2 - ancho_puerta/2

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])