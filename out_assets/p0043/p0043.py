import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
ancho_total = 1.5
alto_total = 2.0
profundidad = 0.3
espesor_panel = 0.025
num_baldas = 5

# --- Creación de los paneles laterales ---
ancho_interior = ancho_total - 2 * espesor_panel

# Lateral Izquierdo
bpy.ops.mesh.primitive_cube_add(
    location=(-ancho_interior / 2 - espesor_panel / 2, 0, alto_total / 2),
    scale=(espesor_panel, profundidad, alto_total)
)
bpy.context.object.name = 'Panel_Izquierdo'

# Lateral Derecho
bpy.ops.mesh.primitive_cube_add(
    location=(ancho_interior / 2 + espesor_panel / 2, 0, alto_total / 2),
    scale=(espesor_panel, profundidad, alto_total)
)
bpy.context.object.name = 'Panel_Derecho'

# --- Creación de las baldas ---
espacio_entre_baldas = alto_total / (num_baldas - 1)

for i in range(num_baldas):
    altura_balda = i * espacio_entre_baldas - (espesor_panel / 2 if i == 0 else 0) + (espesor_panel / 2 if i == num_baldas-1 else 0)
    if i == 0: altura_balda = espesor_panel/2
    if i == num_baldas-1: altura_balda = alto_total - espesor_panel/2

    bpy.ops.mesh.primitive_cube_add(
        location=(0, 0, altura_balda),
        scale=(ancho_interior, profundidad, espesor_panel)
    )
    bpy.context.object.name = f'Balda_{i+1}'