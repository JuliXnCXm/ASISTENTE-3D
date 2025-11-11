import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
largo_brazo1 = 3.0
largo_brazo2 = 2.0
ancho = 0.6
alto = 0.5

# --- Crear primer brazo (en el eje X) ---
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=((largo_brazo1 - ancho) / 2, 0, alto / 2),
    scale=(largo_brazo1 - ancho, ancho, alto)
)
brazo1 = bpy.context.active_object
brazo1.name = "JardineraBrazoLargo"

# --- Crear segundo brazo (en el eje Y) ---
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-ancho / 2, (largo_brazo2) / 2, alto / 2),
    scale=(ancho, largo_brazo2, alto)
)
brazo2 = bpy.context.active_object
brazo2.name = "JardineraBrazoCorto"