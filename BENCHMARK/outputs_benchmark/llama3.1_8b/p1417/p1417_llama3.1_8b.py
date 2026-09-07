import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la pérgola
ancho = 4
alto = 3
profundidad = 2

# Crea las columnas
for i in range(4):
    columna = bpy.data.curves.new('Column', 'MESH')
    columna.dimensions = 'CUBE'
    columna.location = (i * profundidad, 0, 0)
    columna.scale = (alto / 10, alto / 10, alto / 10)
    bpy.context.collection.objects.link(columna)

# Crea el techo
techo = bpy.data.curves.new('Techo', 'MESH')
techo.dimensions = 'QUAD'
techo.location = (0, 0, alto)
techo.scale = (ancho * 2 / 10, profundidad / 10, 1)
bpy.context.collection.objects.link(techo)

# Guarda el archivo .blend si se especificó la ruta
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])