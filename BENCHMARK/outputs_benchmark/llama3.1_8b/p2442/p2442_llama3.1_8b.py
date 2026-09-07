import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de los muros
alto = 2.5
ancho_x = 4
ancho_y = 3

# Crea el primer muro (X)
bpy.ops.mesh.primitive_cube_add(size=alto, location=(0, 0, alto/2))
muro_x = bpy.context.active_object
muro_x.scale = (ancho_x, alto, alto)

# Crea el segundo muro (Y)
bpy.ops.mesh.primitive_cube_add(size=alto, location=(ancho_y/2, 0, alto/2))
muro_y = bpy.context.active_object
muro_y.scale = (ancho_y, alto, alto)

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])