import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la cama
ancho = 1.6
largo = 2.0
alto = 0.5

# Crea el marco superior de madera
marco_superior = bpy.data.objects.new("Marco Superior", None)
marco_superior.location = mathutils.Vector((0, 0, alto))
bpy.context.collection.objects.link(marco_superior)

# Crea los lados del marco superior
lado_derecho_marco_superior = bpy.data.objects.new("Lado Derecho Marco Superior", None)
lado_derecho_marco_superior.location = mathutils.Vector((ancho / 2, 0, alto))
bpy.context.collection.objects.link(lado_derecho_marco_superior)

lado_izquierdo_marco_superior = bpy.data.objects.new("Lado Izquierdo Marco Superior", None)
lado_izquierdo_marco_superior.location = mathutils.Vector((-ancho / 2, 0, alto))
bpy.context.collection.objects.link(lado_izquierdo_marco_superior)

# Crea el marco inferior de madera
marco_inferior = bpy.data.objects.new("Marco Inferior", None)
marco_inferior.location = mathutils.Vector((0, 0, -alto))
bpy.context.collection.objects.link(marco_inferior)

# Crea los lados del marco inferior
lado_derecho_marco_inferior = bpy.data.objects.new("Lado Derecho Marco Inferior", None)
lado_derecho_marco_inferior.location = mathutils.Vector((ancho / 2, 0, -alto))
bpy.context.collection.objects.link(lado_derecho_marco_inferior)

lado_izquierdo_marco_inferior = bpy.data.objects.new("Lado Izquierdo Marco Inferior", None)
lado_izquierdo_marco_inferior.location = mathutils.Vector((-ancho / 2, 0, -alto))
bpy.context.collection.objects.link(lado_izquierdo_marco_inferior)

# Crea los pies de la cama
pie_derecho = bpy.data.objects.new("Pie Derecho", None)
pie_derecho.location = mathutils.Vector((ancho / 2, largo / 2, -alto))
bpy.context.collection.objects.link(pie_derecho)

pie_izquierdo = bpy.data.objects.new("Pie Izquierdo", None)
pie_izquierdo.location = mathutils.Vector((-ancho / 2, largo / 2, -alto))
bpy.context.collection.objects.link(pie_izquierdo)

# Crea el colchón
colchon = bpy.data.objects.new("Colchon", None)
colchon.location = mathutils.Vector((0, 0, 0))
colchon.scale = (ancho, largo, alto / 2)
bpy.context.collection.objects.link(colchon)

# Crea el textil blanco
textil_blanco = bpy.data.objects.new("Textil Blanco", None)
textil_blanco.location = mathutils.Vector((0, 0, -alto))
textil_blanco.scale = (ancho, largo, alto / 2)
bpy.context.collection.objects.link(textil_blanco)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])