import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del muro
longitud = 5  # en metros
altura = 2.8  # en metros
espesor = 0.15  # en metros

# Crea un nuevo objeto para el muro
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, altura/2 + espesor/2))

# Selecciona el objeto creado y lo renombramos
objeto = bpy.context.active_object
objeto.name = "Muro"

# Escalamos el objeto para que tenga las dimensiones correctas
bpy.ops.transform.resize(value=(longitud, altura, espesor))

# Rotamos el objeto 90 grados alrededor del eje Y para que esté en posición vertical
bpy.context.object.rotation_euler = (0, mathutils.pi/2, 0)

# Si existe la variable de entorno BLEND_OUT, guardamos el archivo .blend con ese nombre
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])