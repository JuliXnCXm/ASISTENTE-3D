import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la casa en metros
ancho = 15
profundo = 7.33
altura_muro = 3
altura_piso = 0.2

# Crea el suelo
bpy.ops.mesh.primitive_plane_add(size=110, location=(0, 0, -1))
bpy.context.active_object.name = "Suelo"

# Crea los muros de la zona de día
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(-5.65, 3.66, altura_muro))
bpy.context.active_object.name = "Muro_Dia_1"
bpy.ops.transform.resize(value=(ancho, ancho, altura_piso))

bpy.ops.mesh.primitive_cube_add(size=profundo, location=(-5.65, -4.67, altura_muro))
bpy.context.active_object.name = "Muro_Dia_2"
bpy.ops.transform.resize(value=(profundo, profundo, altura_piso))

# Crea los muros de la zona de noche
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(-5.65, -4.67, altura_muro))
bpy.context.active_object.name = "Muro_Noche_1"
bpy.ops.transform.resize(value=(ancho, ancho, altura_piso))

bpy.ops.mesh.primitive_cube_add(size=profundo, location=(-5.65, 3.66, altura_muro))
bpy.context.active_object.name = "Muro_Noche_2"
bpy.ops.transform.resize(value=(profundo, profundo, altura_piso))

# Crea el patio
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(-5.65, 0, altura_muro))
bpy.context.active_object.name = "Patio"
bpy.ops.transform.resize(value=(ancho, ancho, altura_piso))

# Crea la isla de cocina
bpy.ops.mesh.primitive_cube_add(size=2, location=(-4.33, -3.67, altura_muro))
bpy.context.active_object.name = "Isla_Cocina"
bpy.ops.transform.resize(value=(2, 2, altura_piso))

# Crea la mesa de comedor
bpy.ops.mesh.primitive_cube_add(size=1.5, location=(-4.33, -3.67, altura_muro))
bpy.context.active_object.name = "Mesa_Comedor"
bpy.ops.transform.resize(value=(1.5, 1.5, altura_piso))

# Crea el sofá
bpy.ops.mesh.primitive_cube_add(size=2, location=(-4.33, -3.67, altura_muro))
bpy.context.active_object.name = "Sofa"
bpy.ops.transform.resize(value=(2, 2, altura_piso))

# Crea las camas
bpy.ops.mesh.primitive_cube_add(size=1.5, location=(-4.33, -3.67, altura_muro))
bpy.context.active_object.name = "Cama_1"
bpy.ops.transform.resize(value=(1.5, 1.5, altura_piso))

bpy.ops.mesh.primitive_cube_add(size=1.5, location=(-4.33, -3.67, altura_muro))
bpy.context.active_object.name = "Cama_2"
bpy.ops.transform.resize(value=(1.5, 1.5, altura_piso))

# Guarda el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])