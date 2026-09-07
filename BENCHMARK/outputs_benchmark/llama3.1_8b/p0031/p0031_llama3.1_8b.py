import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la losa en metros
longitud = 6
ancho = 4
espesor = 0.20

# Crea un nuevo objeto para la losa
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))

# Selecciona el objeto creado
objeto = bpy.context.active_object

# Establece las dimensiones de la losa
objeto.dimensions = (longitud, ancho, espesor)

# Renombra el objeto a 'piso'
bpy.ops.object.rename(object=objeto, new_name='piso')

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])