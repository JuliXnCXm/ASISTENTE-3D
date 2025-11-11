import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
altura = 2.5
espesor = 0.15
largo_x = 4.0
largo_y = 3.0

# --- Muro en dirección X (Norte) ---
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_x / 2, espesor / 2, altura / 2),
    scale=(largo_x, espesor, altura)
)
bpy.context.object.name = 'Muro_Norte'

# --- Muro en dirección Y (Oeste) ---
# Se ajusta la posición para que sea contiguo y forme la esquina
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-espesor / 2, (largo_y / 2) + espesor, altura / 2),
    scale=(espesor, largo_y, altura)
)
bpy.context.object.name = 'Muro_Oeste'