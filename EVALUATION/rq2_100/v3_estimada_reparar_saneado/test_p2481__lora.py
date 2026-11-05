import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
largo_muro1 = 5.0
largo_muro2 = 4.0
alto_muro = 2.7
espesor_muro = 0.2
grosor_losa = 0.2

# --- Crear Losa de Piso ---
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, -grosor_losa / 2),
    scale=(largo_muro1 + espesor_muro, largo_muro2 + espesor_muro, grosor_losa)
)
bpy.context.object.name = "Losa_Piso"

# --- Crear Muro 1 (a lo largo del eje X) ---
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_muro1 / 2, -espesor_muro / 2, alto_muro / 2),
    scale=(largo_muro1, espesor_muro, alto_muro)
)
bpy.context.object.name = "Muro_Largo"

# --- Crear Muro 2 (a lo largo del eje Y) ---
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-espesor_muro / 2, largo_muro2 / 2, alto_muro / 2),
    scale=(espesor_muro, largo_muro2, alto_muro)
)
bpy.context.object.name = "Muro_Corto"