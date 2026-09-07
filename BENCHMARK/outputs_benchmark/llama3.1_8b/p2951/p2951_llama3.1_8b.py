import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la plaza
ancho = 12
alto = 10

# Crea el suelo base
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
suelo_base = bpy.context.active_object
suelo_base.scale = (ancho, alto, 0.01)

# Define las dimensiones de los bancos
banco_ancho = 2.0
banco_alto = 1.5
banco_profundidad = 0.5

# Crea el primer banco
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho/2 - banco_ancho/2, 0, 0))
asiento_izquierdo = bpy.context.active_object
asiento_izquierdo.scale = (banco_ancho, banco_alto, banco_profundidad)
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho/2 - banco_ancho/2 + 4, 0, 0))
respaldo_izquierdo = bpy.context.active_object
respaldo_izquierdo.scale = (banco_ancho, banco_alto, banco_profundidad)

# Crea el segundo banco
bpy.ops.mesh.primitive_cube_add(size=1, location=(-ancho/2 + banco_ancho/2, 0, 0))
asiento_derecho = bpy.context.active_object
asiento_derecho.scale = (banco_ancho, banco_alto, banco_profundidad)
bpy.ops.mesh.primitive_cube_add(size=1, location=(-ancho/2 + banco_ancho/2 - 4, 0, 0))
respaldo_derecho = bpy.context.active_object
respaldo_derecho.scale = (banco_ancho, banco_alto, banco_profundidad)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])