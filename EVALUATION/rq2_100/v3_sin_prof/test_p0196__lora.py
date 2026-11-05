import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
ancho_fachada = 6.0
alto_fachada = 4.0
mod_x = 2.0
mod_y = 2.0
grosor_montante = 0.1
grosor_travesano = 0.1
ancho_panel = mod_x - grosor_montante
alto_panel = mod_y - grosor_travesano

# --- Crear Montantes Verticales ---
num_montantes = int(ancho_fachada / mod_x) + 1
for i in range(num_montantes):
    pos_x = i * mod_x - ancho_fachada / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, alto_fachada / 2),
        scale=(grosor_montante, grosor_travesano, alto_fachada)
    )
    bpy.context.object.name = f'Montante_{i}'

# --- Crear Travesaños Horizontales ---
num_travesanos = int(alto_fachada / mod_y) + 1
for i in range(num_travesanos):
    pos_z = i * mod_y
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, pos_z),
        scale=(ancho_fachada, grosor_travesano, grosor_montante)
    )
    bpy.context.object.name = f'Travesano_{i}'

# --- Crear Paneles de Vidrio ---
num_paneles_x = num_montantes - 1
num_paneles_y = num_travesanos - 1
for i in range(num_paneles_x):
    for j in range(num_paneles_y):
        pos_x = i * mod_x + grosor_montante / 2
        pos_z = j * mod_y + grosor_travesano / 2
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(pos_x, 0, pos_z),
            scale=(ancho_panel, 0.01, alto_panel)
        )
        bpy.context.object.name = f'Panel_Vidrio_{i}_{j}'