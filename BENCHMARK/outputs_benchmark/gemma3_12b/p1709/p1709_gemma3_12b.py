import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la terraza (metros)
longitud = 6.0
ancho = 4.0
altura = 0.1  # Altura de la terraza
altura_baranda = 0.9
grosor_plataforma = 0.05

# Crear la plataforma de la terraza
bpy.ops.mesh.primitive_plane_add(size=longitud, enter_editmode=False, align='WORLD', location=(0, 0, altura), scale=(1, ancho/longitud, 1))
plataforma = bpy.context.object
plataforma.name = "Terraza"
plataforma.data.name = "Terraza_Mesh"

# Subdividir la plataforma para la baranda
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=10)
bpy.ops.object.mode_set(mode='OBJECT')

# Crear la baranda
bpy.ops.mesh.primitive_cube_add(size=0.1, enter_editmode=False, align='WORLD', location=(longitud/2, 0, altura + altura_baranda/2), scale=(1, 1, 1))
baranda = bpy.context.object
baranda.name = "Baranda"
baranda.data.name = "Baranda_Mesh"
baranda.scale[0] = longitud/2 - 0.1
baranda.scale[1] = 0.1
baranda.scale[2] = altura_baranda

# Mover la baranda a un lado largo
baranda.location[0] = longitud/2

# Crear pilares para la baranda
def crear_pilar(x, y, z, ancho, alto, profundo):
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(x, y, z), scale=(1, 1, 1))
    pilar = bpy.context.object
    pilar.name = "Pilar_Baranda"
    pilar.data.name = "Pilar_Baranda_Mesh"
    pilar.scale[0] = ancho
    pilar.scale[1] = alto
    pilar.scale[2] = profundo

crear_pilar(longitud/2 - 0.05, 0, altura + altura_baranda/2, 0.1, altura_baranda, 0.1)
crear_pilar(-longitud/2 + 0.05, 0, altura + altura_baranda/2, 0.1, altura_baranda, 0.1)

# Ajustar el grosor de la plataforma
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, -grosor_plataforma)})
bpy.ops.object.mode_set(mode='OBJECT')

# Guardar el archivo .blend si BLEND_OUT está definido
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])