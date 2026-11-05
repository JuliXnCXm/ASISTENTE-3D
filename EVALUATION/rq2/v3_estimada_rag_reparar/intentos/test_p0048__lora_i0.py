import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del falso techo ---
ancho_techo = 6.0
fondo_techo = 4.0
espesor_techo = 0.2
altura_suspension = 2.8
ancho_perfil = 0.05
num_filas = 6
num_columnas = 4

# --- Crear el plano base del falso techo ---
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, altura_suspension))
techo_base = bpy.context.active_object
techo_base.name = 'TechoBase'
techo_base.dimensions = (ancho_techo, fondo_techo, espesor_techo)

# --- Crear perfiles verticales ---
espacio_vertical = ancho_techo / (num_filas - 1)
for i in range(num_filas):
    pos_x = -ancho_techo / 2 + ancho_perfil / 2 + i * espacio_vertical
    bpy.ops.mesh.primitive_cube_add(location=(pos_x, 0, altura_suspension + espesor_techo / 2))
    perfil_v = bpy.context.active_object
    perfil_v.name = f'PerfilVertical_{i}'
    perfil_v.dimensions = (ancho_perfil, fondo_techo, espesor_techo)

# --- Crear perfiles horizontales ---
espacio_horizontal = fondo_techo / (num_columnas - 1)
for i in range(num_columnas):
    pos_z = altura_suspension + espesor_techo / 2 + i * espacio_horizontal
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, pos_z))
    perfil_h = bpy.context.active_object
    perfil_h.name = f'PerfilHorizontal_{i}'
    perfil_h.dimensions = (ancho_techo, ancho_perfil, espesor_techo)

# --- Añadir iluminación ---
bpy.ops.object.light_add(type='POINT', radius=1, location=(-ancho_techo/2, -fondo_techo/2, altura_suspension + 1.5))
luz1 = bpy.context.active_object
luz1.data.energy = 150

bpy.ops.object.light_add(type='POINT', radius=1, location=(ancho_techo/2, -fondo_techo/2, altura_suspension + 1.5))
luz2 = bpy.context.active_object
luz2.data.energy = 150

bpy.ops.object.light_add(type='POINT', radius=1, location=(-ancho_techo/2, fondo_techo/2, altura_suspension + 1.5))
luz3 = bpy.context.active_object
luz3.data.energy = 150

bpy.ops.object.light_add(type='POINT', radius=1, location=(ancho_techo/2, fondo_techo/2, altura_suspension + 1.5))
luz4 = bpy.context.active_object
luz4.data.energy = 150