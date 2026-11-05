import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

ancho_total = 6.0
alto_total = 9.0
dist_horizontal = 1.5
dist_vertical = 3.0
ancho_perfil = 0.1
espesor_vidrio = 0.02

# Crear Montantes (verticales)
num_montantes = int(ancho_total / dist_horizontal) + 1
for i in range(num_montantes):
    pos_x = i * dist_horizontal
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, ancho_perfil / 2, alto_total / 2),
        scale=(ancho_perfil, ancho_perfil, alto_total)
    )
    bpy.context.active_object.name = f'Montante_{i+1}'

# Crear Travesaños (horizontales)
num_travesanos = int(alto_total / dist_vertical) + 1
for i in range(num_travesanos):
    pos_z = i * dist_vertical
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(ancho_total / 2, ancho_perfil / 2, pos_z),
        scale=(ancho_total, ancho_perfil, ancho_perfil)
    )
    bpy.context.active_object.name = f'Travesano_{i+1}'

# Crear Paneles de Vidrio
num_paneles_x = int(ancho_total / dist_horizontal)
num_paneles_y = int(alto_total / dist_vertical)

for i in range(num_paneles_x):
    for j in range(num_paneles_y):
        centro_x = i * dist_horizontal + dist_horizontal / 2
        centro_z = j * dist_vertical + dist_vertical / 2
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(centro_x, 0, centro_z),
            scale=(dist_horizontal - ancho_perfil, espesor_vidrio, dist_vertical - ancho_perfil)
        )
        bpy.context.active_object.name = f'Vidrio_{i+1}_{j+1}'