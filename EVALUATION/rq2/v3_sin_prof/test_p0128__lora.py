import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la estantería ---
alto_total = 1.8
ancho_total = 0.8
profundidad_total = 0.3
num_estantes = 5
grosor_panel = 0.02
espesor_poste = 0.02

# --- Creación de paneles verticales (postes) ---
ancho_poste = ancho_total / (num_estantes + 1)
for i in range(num_estantes + 1):
    pos_x = -ancho_total / 2 + ancho_poste / 2 + i * ancho_poste
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, alto_total / 2),
        scale=(espesor_poste, profundidad_total, alto_total)
    )
    poste = bpy.context.active_object
    poste.name = f"Poste_{i}"

# --- Creación de estantes ---
espacio_entre_estantes = alto_total / (num_estantes)
for i in range(num_estantes):
    altura_estante = i * espacio_entre_estantes
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, altura_estante + grosor_panel / 2),
        scale=(ancho_total, profundidad_total, grosor_panel)
    )
    estante = bpy.context.active_object
    estante.name = f"Estante_{i}"