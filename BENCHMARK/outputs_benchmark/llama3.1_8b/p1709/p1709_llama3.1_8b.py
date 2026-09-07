import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la terraza
ancho = 6
largo = 4
altura = 0.5

# Crea el plano de la terraza
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, altura))
terraza = bpy.context.active_object
terraza.name = "Terraza"

# Aplica la escala a la terraza
terraza.scale = (ancho, largo, 1)

# Crea el plano de la baranda
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, ancho/2, altura + 0.5))
baranda = bpy.context.active_object
baranda.name = "Baranda"

# Aplica la escala a la baranda
baranda.scale = (ancho, 0.1, 1)

# Rotación de la baranda para que quede en el lado correcto
baranda.rotation_euler = mathutils.Vector((math.radians(90), 0, 0))

# Ubicación de la baranda
baranda.location = (largo/2, ancho/4, altura + 0.5)

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])