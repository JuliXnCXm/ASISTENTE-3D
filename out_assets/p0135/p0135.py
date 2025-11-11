import bpy
import math

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Parámetros de la retícula
area_x = 4.0
area_y = 3.0
altura_z = 2.6
modulo = 0.6
ancho_perfil = 0.05
alto_perfil = 0.05

# Crear perfiles a lo largo del eje X
num_perfiles_y = math.ceil(area_y / modulo) + 1
for i in range(num_perfiles_y):
    pos_y = (i * modulo) - (area_y / 2)
    if pos_y > area_y/2:
        pos_y = area_y/2

    bpy.ops.mesh.primitive_cube_add(
        location=(0, pos_y, altura_z),
        scale=(area_x / 2, ancho_perfil / 2, alto_perfil / 2)
    )
    bpy.context.object.name = f"Perfil_X_{i}"

# Crear perfiles a lo largo del eje Y
num_perfiles_x = math.ceil(area_x / modulo) + 1
for i in range(num_perfiles_x):
    pos_x = (i * modulo) - (area_x / 2)
    if pos_x > area_x/2:
        pos_x = area_x/2

    bpy.ops.mesh.primitive_cube_add(
        location=(pos_x, 0, altura_z),
        scale=(ancho_perfil / 2, area_y / 2, alto_perfil / 2)
    )
    bpy.context.object.name = f"Perfil_Y_{i}"