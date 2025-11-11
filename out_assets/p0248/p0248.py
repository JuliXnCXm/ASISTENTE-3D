import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones generales
ancho_total = 6.0
alto_total = 5.0
ancho_modulo = 1.5
alto_modulo = 2.5
grosor_perfil = 0.1
grosor_vidrio = 0.02

num_modulos_h = int(ancho_total / ancho_modulo)
num_modulos_v = int(alto_total / alto_modulo)

# Crear montantes (verticales)
for i in range(num_modulos_h + 1):
    pos_x = i * ancho_modulo
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, alto_total / 2),
        scale=(grosor_perfil, grosor_perfil, alto_total)
    )
    bpy.context.object.name = f'Montante_{i}'

# Crear travesaños (horizontales)
for i in range(num_modulos_v + 1):
    pos_z = i * alto_modulo
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(ancho_total / 2, 0, pos_z),
        scale=(ancho_total + grosor_perfil, grosor_perfil, grosor_perfil)
    )
    bpy.context.object.name = f'Travesano_{i}'

# Crear paneles de vidrio
for i in range(num_modulos_h):
    for j in range(num_modulos_v):
        pos_x_panel = (i + 0.5) * ancho_modulo
        pos_z_panel = (j + 0.5) * alto_modulo
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(pos_x_panel, 0, pos_z_panel),
            scale=(ancho_modulo - grosor_perfil, grosor_vidrio, alto_modulo - grosor_perfil)
        )
        bpy.context.object.name = f'Vidrio_{i}_{j}'