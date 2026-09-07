import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la pérgola
ancho = 4
alto = 3
profundidad = 1

# Crea las columnas
for i in range(4):
    columna = bpy.data.curves.new('Columna', 'MESH')
    columna.dimensions = 'CUBE'
    columna.location = (i * ancho, 0, 0)
    columna.scale = (alto / 2, alto / 2, profundidad)
    bpy.context.collection.objects.link(columna)

# Crea el techo
techo = bpy.data.curves.new('Techo', 'MESH')
techo.dimensions = 'CUBE'
techo.location = ((ancho - 1) / 2, (alto - 1) / 2, profundidad)
techo.scale = (ancho, alto, profundidad)
bpy.context.collection.objects.link(techo)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])