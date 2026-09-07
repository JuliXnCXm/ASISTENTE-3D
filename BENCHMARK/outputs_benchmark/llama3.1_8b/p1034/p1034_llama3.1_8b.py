import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la cama
ancho = 1.6
largo = 2.0

# Crea el marco de madera
marco = bpy.data.objects.new("Marco", None)
marco.empty_display_size = 0.5
bpy.context.collection.objects.link(marco)

# Agrega los lados del marco
for i in range(4):
    lado = bpy.data.objects.new(f"Lado {i}", None)
    lado.empty_display_size = 0.1
    lado.location = mathutils.Vector((ancho / 2, largo / 2, 0)) if i == 0 else \
                    mathutils.Vector((-ancho / 2, largo / 2, 0)) if i == 1 else \
                    mathutils.Vector((ancho / 2, -largo / 2, 0)) if i == 2 else \
                    mathutils.Vector((-ancho / 2, -largo / 2, 0))
    bpy.context.collection.objects.link(lado)

# Agrega los ángulos del marco
for i in range(4):
    angulo = bpy.data.objects.new(f"Ángulo {i}", None)
    angulo.empty_display_size = 0.1
    angulo.location = mathutils.Vector((ancho / 2, largo / 2, 0)) if i == 0 else \
                      mathutils.Vector((-ancho / 2, largo / 2, 0)) if i == 1 else \
                      mathutils.Vector((ancho / 2, -largo / 2, 0)) if i == 2 else \
                      mathutils.Vector((-ancho / 2, -largo / 2, 0))
    bpy.context.collection.objects.link(angulo)

# Crea el colchón
colchon = bpy.data.objects.new("Colchón", None)
colchon.empty_display_size = 1.5
colchon.location = mathutils.Vector((ancho / 2, largo / 2, 0))
bpy.context.collection.objects.link(colchon)

# Aplica materiales al marco y colchón
marco.data.materials.append(bpy.data.materials['Material_Roble'])
colchon.data.materials.append(bpy.data.materials['Material_Tela_Blanca'])

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.context.scene.BLEND_OUT)