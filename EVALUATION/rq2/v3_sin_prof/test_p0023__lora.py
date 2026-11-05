import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
alto_total = 1.8
ancho_total = 0.9
fondo_total = 0.3
num_baldas = 5
grosor_panel = 0.02
espesor_poste = 0.02

# --- Creación de Baldas ---
espacio_entre_baldas = alto_total / (num_baldas + 1)
for i in range(num_baldas):
    z_pos = i * espacio_entre_baldas
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(ancho_total/2, fondo_total/2, z_pos),
        scale=(ancho_total, grosor_panel, grosor_panel)
    )
    bpy.context.active_object.name = f"Baldas_{i+1}"

# --- Creación de Postes ---
posiciones_x = [espesor_poste, ancho_total - espesor_poste]
posiciones_z = [0, alto_total]

for x_pos in posiciones_x:
    for z_pos in posiciones_z:
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(x_pos, fondo_total/2, z_pos),
            scale=(espesor_poste, fondo_total, alto_total)
        )
        bpy.context.active_object.name = f"Poste_{z_pos}"

        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(ancho_total/2, x_pos, z_pos),
            scale=(ancho_total, espesor_poste, alto_total)
        )
        bpy.context.active_object.name = f"Poste_{z_pos}_2"