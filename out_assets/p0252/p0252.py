import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la losa ---
largo = 10.0
ancho = 8.0
espesor = 0.3

# --- Creación de la losa ---
# Se crea en el origen, su base estará en z=-espesor/2
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, espesor / 2) # Elevamos para que la base esté en z=0
)
losa = bpy.context.active_object
losa.name = "LosaCimentacion"
losa.dimensions = (largo, ancho, espesor)