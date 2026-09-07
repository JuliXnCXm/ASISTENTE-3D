import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades en metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea un plano para el terreno de césped
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))

# Selecciona el plano y lo renombramos a "césped"
obj_cesped = bpy.context.active_object
obj_cesped.name = 'Césped'

# Establece las dimensiones del terreno en metros
obj_cesped.dimensions = (20, 15, 0.01)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])