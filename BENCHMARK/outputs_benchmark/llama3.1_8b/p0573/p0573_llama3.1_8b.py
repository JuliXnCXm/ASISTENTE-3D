import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del terreno en metros
ancho = 20
alto = 15

# Crea un plano para el terreno
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))

# Selecciona el plano recién creado
bpy.context.active_object.name = "Terreno"

# Aplica una transformación de escala para ajustar las dimensiones del terreno
bpy.context.object.scale = (ancho, alto, 1)

# Define la altura del césped en metros
altura_cespillo = 0.01

# Crea un objeto vacío para el céspillo
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -altura_cespillo))

# Selecciona el cubo recién creado
bpy.context.active_object.name = "Cespillo"

# Aplica una transformación de escala para ajustar las dimensiones del céspillo
bpy.context.object.scale = (ancho, alto, altura_cespillo)

# Combina el plano y el cubo en un solo objeto
bpy.ops.object.join()

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend con ese nombre
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])