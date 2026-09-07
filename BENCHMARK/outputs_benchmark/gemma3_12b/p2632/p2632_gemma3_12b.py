import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la columna
width = 0.4
depth = 0.4
height = 2.8

# Crear la geometría de la columna
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, height/2), scale=(width, depth, height))
columna = bpy.context.object
columna.name = "Columna"

# Escalar el cubo para obtener las dimensiones deseadas
columna.scale = (width/2, depth/2, height/2)

# Centrar la columna en el origen
#bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS') # Ya está centrada al crearla

# Guardar el archivo .blend si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])