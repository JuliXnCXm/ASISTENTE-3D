import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
alto_total = 1.8
ancho_total = 0.8
profundidad_total = 0.3
num_baldas = 5
espesor_panel = 0.02

# --- Creación de paneles verticales ---
ancho_balda = ancho_total / num_baldas
for i in range(num_baldas + 1):
    pos_x = -ancho_total / 2 + ancho_balda * i
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, alto_total / 2),
        scale=(espesor_panel, profundidad_total, alto_total)
    )
    bpy.context.object.name = f"Panel_Vertical_{i}"

# --- Creación de baldas ---
espacio_entre_baldas = alto_total / (num_baldas - 1)
for i in range(num_baldas):
    altura_balda = i * espacio_entre_baldas
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, altura_balda),
        scale=(ancho_total, profundidad_total, espesor_panel)
    )
    bpy.context.object.name = f"Baldas_{i}"