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

# --- Montantes (verticales) ---
num_montantes = int(ancho_fachada / mod_x)
for i in range(num_montantes + 1):
    pos_x = i * mod_x - ancho_fachada / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, alto_fachada / 2),
        scale=(grosor_montante, grosor_travesano, alto_fachada)
    )
    bpy.context.object.name = f"Montante_{i}"

# --- Travesaños (horizontales) ---
num_travesanos = int(alto_fachada / mod_y)
for i in range(num_travesanos + 1):
    pos_z = i * mod_y
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, pos_z),
        scale=(ancho_fachada, grosor_travesano, grosor_montante)
    )
    bpy.context.object.name = f"Travesano_{i}"

# --- Paneles de vidrio ---
for i in range(num_montantes):
    for j in range(num_travesanos):
        x0 = i * mod_x - ancho_fachada / 2 + ancho_panel / 2
        y0 = j * mod_y - grosor_montante / 2
        z0 = 0
        
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x0, y0, z0),
            scale=(ancho_panel, grosor_montante, alto_panel)
        )
        bpy.context.object.name = f"Panel_Vidrio_{i}_{j}"