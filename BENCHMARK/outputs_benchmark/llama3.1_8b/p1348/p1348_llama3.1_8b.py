import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del terreno
ancho = 15
alto = 15

# Crea un plano para el terreno
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))

# Obtiene la geometría del plano
objeto = bpy.context.active_object

# Establece las dimensiones del terreno en metros
objeto.scale = (ancho, alto, 1)

# Renombra el objeto a "Terreno"
bpy.ops.object.rename(object=objeto.name, new_name="Terreno")

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.context.blend_file.use_save_incremental = True
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])