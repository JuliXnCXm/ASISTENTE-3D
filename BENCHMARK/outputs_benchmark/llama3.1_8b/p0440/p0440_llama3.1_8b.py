import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las propiedades de la cama
length = 1.8  # metros
width = 0.9   # metros
height = 0.5  # metros
thickness = 0.01  # metros

# Crea el colchón blanco
colchon = bpy.data.objects.new("Colchon", None)
colchon.location = (0, 0, height)
colchon.scale = (length, width, thickness)
bpy.context.collection.objects.link(colchon)

# Crea la estructura de madera de roble para el colchón
estructura = bpy.data.objects.new("Estructura", None)
estructura.location = (0, 0, height + thickness)
estructura.scale = (length - 2 * thickness, width - 2 * thickness, thickness)
bpy.context.collection.objects.link(estructura)

# Crea los cuatro patas de la cama
pata1 = bpy.data.objects.new("Pata1", None)
pata1.location = (-length/2 + thickness, -width/2 + thickness, height + 2 * thickness)
pata1.scale = (thickness, thickness, thickness)
bpy.context.collection.objects.link(pata1)

pata2 = bpy.data.objects.new("Pata2", None)
pata2.location = (length/2 - thickness, -width/2 + thickness, height + 2 * thickness)
pata2.scale = (thickness, thickness, thickness)
bpy.context.collection.objects.link(pata2)

pata3 = bpy.data.objects.new("Pata3", None)
pata3.location = (-length/2 + thickness, width/2 - thickness, height + 2 * thickness)
pata3.scale = (thickness, thickness, thickness)
bpy.context.collection.objects.link(pata3)

pata4 = bpy.data.objects.new("Pata4", None)
pata4.location = (length/2 - thickness, width/2 - thickness, height + 2 * thickness)
pata4.scale = (thickness, thickness, thickness)
bpy.context.collection.objects.link(pata4)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])