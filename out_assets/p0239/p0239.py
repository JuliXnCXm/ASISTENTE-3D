import bpy

import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones generales
ancho_fachada = 12.0
alto_fachada = 8.0

# Dimensiones de la retícula
mod_x = 2.0
mod_y = 2.0

# Dimensiones de los perfiles y vidrio
ancho_perfil = 0.05
prof_perfil = 0.10
espesor_vidrio = 0.02

num_x = int(ancho_fachada / mod_x)
num_y = int(alto_fachada / mod_y)

# Crear montantes (verticales)
for i in range(num_x + 1):
    x = i * mod_x
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x, prof_perfil / 2, alto_fachada / 2),
        scale=(ancho_perfil, prof_perfil, alto_fachada)
    )
    bpy.context.active_object.name = f"Montante_{i}"

# Crear travesaños (horizontales)
for i in range(num_y + 1):
    y = i * mod_y
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(ancho_fachada / 2, prof_perfil / 2, y),
        scale=(ancho_fachada, prof_perfil, ancho_perfil)
    )
    bpy.context.active_object.name = f"Travesano_{i}"

# Crear paneles de vidrio
panel_ancho = mod_x - ancho_perfil
panel_alto = mod_y - ancho_perfil
for i in range(num_x):
    for j in range(num_y):
        x = i * mod_x + mod_x / 2
        z = j * mod_y + mod_y / 2
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x, prof_perfil / 2, z),
            scale=(panel_ancho, espesor_vidrio, panel_alto)
        )
        bpy.context.active_object.name = f"PanelVidrio_{i}_{j}"