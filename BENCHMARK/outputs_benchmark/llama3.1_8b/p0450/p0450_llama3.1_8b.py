import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las propiedades de la geometría
length = 2.0  # metros
width = 1.5  # metros
height = 0.3  # metros
thickness = 0.05  # metros

# Crea el colchón blanco
colchon = bpy.data.objects.new("Colchon", None)
colchon.location = mathutils.Vector((0, 0, height))
colchon.scale = (length, width, thickness)
bpy.context.collection.objects.link(colchon)

# Crea la estructura de madera del colchón
estructura = bpy.data.objects.new("Estructura", None)
estructura.location = mathutils.Vector((0, 0, height))
estructura.scale = (length, width, thickness)
bpy.context.collection.objects.link(estructura)

# Crea los lados laterales de la estructura
lado_derecho = bpy.data.objects.new("LadoDerecho", None)
lado_derecho.location = mathutils.Vector((length / 2, 0, height))
lado_derecho.scale = (thickness, width, thickness)
bpy.context.collection.objects.link(lado_derecho)

lado_izquierdo = bpy.data.objects.new("LadoIzquierdo", None)
lado_izquierdo.location = mathutils.Vector((-length / 2, 0, height))
lado_izquierdo.scale = (thickness, width, thickness)
bpy.context.collection.objects.link(lado_izquierdo)

# Crea los lados frontales y traseros de la estructura
lado_frontal = bpy.data.objects.new("LadoFrontal", None)
lado_frontal.location = mathutils.Vector((0, width / 2, height))
lado_frontal.scale = (length, thickness, thickness)
bpy.context.collection.objects.link(lado_frontal)

lado_trasero = bpy.data.objects.new("LadoTrasero", None)
lado_trasero.location = mathutils.Vector((0, -width / 2, height))
lado_trasero.scale = (length, thickness, thickness)
bpy.context.collection.objects.link(lado_trasero)

# Crea los lados laterales de la estructura
lado_superior_derecho = bpy.data.objects.new("LadoSuperiorDerecho", None)
lado_superior_derecho.location = mathutils.Vector((length / 2, width / 2, height))
lado_superior_derecho.scale = (thickness, thickness, thickness)
bpy.context.collection.objects.link(lado_superior_derecho)

lado_superior_izquierdo = bpy.data.objects.new("LadoSuperiorIzquierdo", None)
lado_superior_izquierdo.location = mathutils.Vector((-length / 2, width / 2, height))
lado_superior_izquierdo.scale = (thickness, thickness, thickness)
bpy.context.collection.objects.link(lado_superior_izquierdo)

lado_inferior_derecho = bpy.data.objects.new("LadoInferiorDerecho", None)
lado_inferior_derecho.location = mathutils.Vector((length / 2, -width / 2, height))
lado_inferior_derecho.scale = (thickness, thickness, thickness)
bpy.context.collection.objects.link(lado_inferior_derecho)

lado_inferior_izquierdo = bpy.data.objects.new("LadoInferiorIzquierdo", None)
lado_inferior_izquierdo.location = mathutils.Vector((-length / 2, -width / 2, height))
lado_inferior_izquierdo.scale = (thickness, thickness, thickness)
bpy.context.collection.objects.link(lado_inferior_izquierdo)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])