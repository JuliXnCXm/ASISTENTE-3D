import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del terreno en metros
ancho = 20
alto = 30

# Crea un plano para el terreno
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))

# Obtiene la geometría del plano
objeto = bpy.context.active_object

# Establece las dimensiones del plano en metros
objeto.scale = (ancho, alto, 0.01)

# Cambia el nombre del objeto a "Terreno"
bpy.ops.object.rename(object=objeto.name, new_name="Terreno")

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])