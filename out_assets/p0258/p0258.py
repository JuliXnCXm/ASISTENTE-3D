import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del muro cortina ---
ancho_total = 5.0
alto_total = 3.0
num_modulos_x = 5
num_modulos_y = 3
grosor_perfil = 0.05
profundidad_perfil = 0.1

# --- Creación de montantes (verticales) ---
ancho_modulo = ancho_total / num_modulos_x
for i in range(num_modulos_x + 1):
    pos_x = (i * ancho_modulo) - (ancho_total / 2)
    bpy.ops.mesh.primitive_cube_add(
        location=(pos_x, 0, alto_total / 2)
    )
    montante = bpy.context.active_object
    montante.name = f"MuroCortina.Montante_{i+1}"
    montante.dimensions = (grosor_perfil, profundidad_perfil, alto_total)

# --- Creación de travesaños (horizontales) ---
alto_modulo = alto_total / num_modulos_y
for i in range(num_modulos_y + 1):
    pos_z = i * alto_modulo
    bpy.ops.mesh.primitive_cube_add(
        location=(0, 0, pos_z)
    )
    travesano = bpy.context.active_object
    travesano.name = f"MuroCortina.Travesano_{i+1}"
    travesano.dimensions = (ancho_total + grosor_perfil, profundidad_perfil, grosor_perfil)

# --- Creación de paneles de vidrio ---
ancho_panel = ancho_modulo - grosor_perfil
alto_panel = alto_modulo - grosor_perfil
for i in range(num_modulos_x):
    for j in range(num_modulos_y):
        pos_x_panel = (i * ancho_modulo) - (ancho_total / 2) + (ancho_modulo / 2)
        pos_z_panel = (j * alto_modulo) + (alto_modulo / 2)
        bpy.ops.mesh.primitive_plane_add(
            size=1,
            location=(pos_x_panel, 0, pos_z_panel)
        )
        panel = bpy.context.active_object
        panel.name = f"MuroCortina.Vidrio_{i+1}_{j+1}"
        panel.dimensions = (ancho_panel, alto_panel, 0)
        panel.rotation_euler[0] = 1.5708 # 90 grados en X