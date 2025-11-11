import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Creación de la losa de cubierta ---
largo = 12.0
ancho = 8.0
espesor = 0.3

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, espesor / 2),
    scale=(largo, ancho, espesor)
)

losa_cubierta = bpy.context.active_object
losa_cubierta.name = "LosaCubiertaPlana"