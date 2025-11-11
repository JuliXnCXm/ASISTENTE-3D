import bpy

bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones generales
ancho_total = 3.0
alto_total = 4.0

# Divisiones
num_mod_x = 3
num_mod_y = 4

# Perfilería
ancho_perfil = 0.05
prof_perfil = 0.10

# Montantes (verticales)
for i in range(num_mod_x + 1):
    pos_x = (i / num_mod_x - 0.5) * ancho_total
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, alto_total / 2),
        scale=(ancho_perfil, prof_perfil, alto_total)
    )
    bpy.context.object.name = f'Montante_{i+1}'

# Travesaños (horizontales)
for i in range(num_mod_y + 1):
    pos_z = (i / num_mod_y) * alto_total
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, pos_z),
        scale=(ancho_total + ancho_perfil, prof_perfil, ancho_perfil)
    )
    bpy.context.object.name = f'Travesano_{i+1}'

# Paneles de vidrio
ancho_panel = ancho_total / num_mod_x - ancho_perfil
alto_panel = alto_total / num_mod_y - ancho_perfil
espesor_vidrio = 0.01

for i in range(num_mod_x):
    for j in range(num_mod_y):
        centro_x = (-ancho_total / 2) + (ancho_perfil / 2) + (ancho_panel / 2) + i * (ancho_panel + ancho_perfil)
        centro_z = (ancho_perfil / 2) + (alto_panel / 2) + j * (alto_panel + ancho_perfil)
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(centro_x, 0, centro_z),
            scale=(ancho_panel, espesor_vidrio, alto_panel)
        )
        bpy.context.object.name = f'Vidrio_{i+1}_{j+1}'