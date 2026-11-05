import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del panel ---
ancho_total = 6.0
alto_total = 3.0
grosor_perfil = 0.1
divisiones_h = 4
divisiones_v = 2
espesor_vidrio = 0.005

# --- Creación de los perfiles verticales (montantes) ---
ancho_div = ancho_total / divisiones_v
for i in range(divisiones_v + 1):
    pos_x = -ancho_total / 2 + ancho_div * i
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, alto_total / 2),
        scale=(grosor_perfil, grosor_perfil, alto_total)
    )
    bpy.context.object.name = f"Montante_{i}"

# --- Creación de los perfiles horizontales (travesaños) ---
alto_div = alto_total / divisiones_h
for i in range(divisiones_h + 1):
    pos_z = -alto_total / 2 + alto_div * i
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, pos_z),
        scale=(ancho_total, grosor_perfil, grosor_perfil)
    )
    bpy.context.object.name = f"Travesano_{i}"

# --- Creación de los paneles de vidrio ---
ancho_panel = ancho_div - grosor_perfil
alto_panel = alto_div - grosor_perfil
for i in range(divisiones_h):
    for j in range(divisiones_v):
        # Calcular posición del panel
        pos_x = -ancho_total / 2 + ancho_div / 2 + ancho_panel * j
        pos_z = -alto_total / 2 + alto_div / 2 + alto_panel * i
        
        # Crear el panel de vidrio
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(pos_x, 0, pos_z),
            scale=(ancho_panel, grosor_perfil, alto_panel)
        )
        bpy.context.object.name = f"Vidrio_{i}_{j}"