import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del patio trasero
ancho = 5
largo = 4

# Crea el piso de concreto
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
piso = bpy.context.active_object
piso.scale = (ancho, largo, 0.01)  # Ajusta la escala del piso

# Crea el muro de ladrillo
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.5))
muro = bpy.context.active_object
muro.scale = (ancho, largo, 2)  # Ajusta la escala del muro

# Ajusta la posición del muro para que esté en el fondo del patio
muro.location = (0, 0, -1)

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])