import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
ancho = 2.4
profundidad = 0.9
altura_total = 0.7
altura_base = 0.25
espesor_reposabrazos = 0.2
altura_cojin = 0.15

# --- Base del sofá ---
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, altura_base / 2),
    scale=(ancho, profundidad, altura_base)
)
bpy.context.object.name = 'Base_Sofa'

# --- Respaldo ---
altura_respaldo = altura_total - (altura_base + altura_cojin)
profundidad_respaldo = 0.15
bpy.ops.mesh.primitive_cube_add(
    location=(0, -profundidad/2 + profundidad_respaldo/2, altura_base + altura_cojin + altura_respaldo/2),
    scale=(ancho, profundidad_respaldo, altura_respaldo)
)
bpy.context.object.name = 'Respaldo_Sofa'

# --- Reposabrazos ---
ancho_interior = ancho - 2 * espesor_reposabrazos
altura_reposabrazos = 0.3
# Reposabrazos Izquierdo
bpy.ops.mesh.primitive_cube_add(
    location=(-ancho/2 + espesor_reposabrazos/2, 0, altura_base + altura_reposabrazos/2),
    scale=(espesor_reposabrazos, profundidad, altura_reposabrazos)
)
bpy.context.object.name = 'Reposabrazos_Izq'
# Reposabrazos Derecho
bpy.ops.mesh.primitive_cube_add(
    location=(ancho/2 - espesor_reposabrazos/2, 0, altura_base + altura_reposabrazos/2),
    scale=(espesor_reposabrazos, profundidad, altura_reposabrazos)
)
bpy.context.object.name = 'Reposabrazos_Der'

# --- Cojines de asiento ---
ancho_cojin = ancho_interior / 3
profundidad_cojin = profundidad - profundidad_respaldo
for i in range(3):
    pos_x = -ancho_interior/2 + ancho_cojin/2 + i*ancho_cojin
    bpy.ops.mesh.primitive_cube_add(
        location=(pos_x, -profundidad_respaldo/2, altura_base + altura_cojin/2),
        scale=(ancho_cojin * 0.95, profundidad_cojin, altura_cojin)
    )
    bpy.context.object.name = f'Cojin_{i+1}'