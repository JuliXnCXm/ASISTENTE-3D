import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la habitación ---
largo_int = 5.0
ancho_int = 4.0
altura = 2.8
espesor = 0.2

# --- Cálculo de dimensiones y posiciones exteriores ---
largo_ext = largo_int + 2 * espesor
ancho_ext = ancho_int + 2 * espesor

# --- Muro Norte ---
bpy.ops.mesh.primitive_cube_add(
    location=(largo_int / 2, ancho_int + espesor / 2, altura / 2),
    scale=(largo_int, espesor, altura)
)
bpy.context.object.name = 'Muro_Norte'

# --- Muro Sur ---
bpy.ops.mesh.primitive_cube_add(
    location=(largo_int / 2, -espesor / 2, altura / 2),
    scale=(largo_int, espesor, altura)
)
bpy.context.object.name = 'Muro_Sur'

# --- Muro Este ---
bpy.ops.mesh.primitive_cube_add(
    location=(largo_int + espesor/2, ancho_int / 2, altura / 2),
    scale=(espesor, ancho_ext, altura)
)
bpy.context.object.name = 'Muro_Este'

# --- Muro Oeste ---
bpy.ops.mesh.primitive_cube_add(
    location=(-espesor / 2, ancho_int / 2, altura / 2),
    scale=(espesor, ancho_ext, altura)
)
bpy.context.object.name = 'Muro_Oeste'