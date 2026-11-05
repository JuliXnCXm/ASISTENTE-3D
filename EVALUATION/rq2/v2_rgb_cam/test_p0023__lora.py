import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
alto_total = 1.8
ancho_total = 0.9
fondo_total = 0.3
num_baldas = 5
grosor_panel = 0.02

# Crear panel vertical
ancho_panel = ancho_total / num_baldas
loc_z_panel = alto_total / 2
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, loc_z_panel),
    scale=(ancho_panel, fondo_total, grosor_panel)
)
panel_vertical = bpy.context.active_object
panel_vertical.name = "Panel_Vertical"

# Crear baldas horizontales
espacio_entre_baldas = alto_total / (num_baldas + 1)
for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas + espacio_entre_baldas / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho_total, fondo_total, grosor_panel)
    )
    balda = bpy.context.active_object
    balda.name = f"Balda_{i+1}"