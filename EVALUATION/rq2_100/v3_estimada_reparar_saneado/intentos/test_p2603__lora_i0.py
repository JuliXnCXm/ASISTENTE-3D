import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
ancho_total = 1.2
alto_total = 2.0
profundidad_total = 0.3
num_baldas = 5
espesor_panel = 0.02

# --- Creación de baldas ---
ancho_util = ancho_total - espesor_panel * num_baldas
alto_balsa = alto_total / num_baldas

for i in range(num_baldas):
    z_pos = i * alto_balsa + alto_balsa / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho_util, profundidad_total, alto_balsa)
    )
    bpy.context.object.name = f"Balsa_{i+1}"

# --- Creación de soporte vertical ---
ancho_soporte = espesor_panel
alto_soporte = alto_total
profundidad_soporte = profundidad_total

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto_soporte / 2),
    scale=(ancho_soporte, profundidad_soporte, alto_soporte)
)
bpy.context.object.name = "Soporte"

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, profundidad_total/2 - espesor_panel/2, alto_soporte / 2),
    scale=(ancho_soporte, espesor_panel, alto_soporte)
)
bpy.context.object.name = "Soporte_Segundo"