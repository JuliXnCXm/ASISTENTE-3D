import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
ancho_total = 6.0
alto_total = 9.0
grosor_perfil = 0.1
espesor_vidrio = 0.02
ancho_panel = 1.5
alto_panel = 3.0
num_h = int(ancho_total / ancho_panel)
num_v = int(alto_total / alto_panel)

# --- Creación de Perfiles Verticales ---
for i in range(num_h + 1):
    pos_x = -ancho_total / 2 + i * ancho_panel
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, alto_total / 2),
        scale=(grosor_perfil, 0.05, alto_total)
    )
    bpy.context.object.name = f"Perfil_Vertical_{i}"

# --- Creación de Perfiles Horizontales ---
for j in range(num_v + 1):
    pos_z = -alto_total / 2 + j * alto_panel
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, pos_z),
        scale=(ancho_total, 0.05, grosor_perfil)
    )
    bpy.context.object.name = f"Perfil_Horizontal_{j}"

# --- Creación de Paneles de Vidrio ---
for i in range(num_h):
    for j in range(num_v):
        pos_x = -ancho_total / 2 + i * ancho_panel + ancho_panel / 2
        pos_z = -alto_total / 2 + j * alto_panel + alto_panel / 2
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(pos_x, 0, pos_z),
            scale=(ancho_panel - grosor_perfil, 0.01, alto_panel - grosor_perfil)
        )
        bpy.context.object.name = f"Panel_Vidrio_{i}_{j}"