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
ancho_losa = 6.0

# --- Crear Losa de Piso ---
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, -espesor_muro / 2),
    scale=(ancho_losa, ancho_losa, espesor_muro)
)
losa = bpy.context.active_object
losa.name = "Losa_Piso"

# --- Crear Muro 1 (a lo largo del eje X) ---
loc_x_muro1 = (largo_muro1 / 2) - (espesor_muro / 2)
loc_y_muro1 = 0
loc_z_muro1 = alto_muro / 2
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(loc_x_muro1, loc_y_muro1, loc_z_muro1),
    scale=(largo_muro1, espesor_muro, alto_muro)
)
muro1 = bpy.context.active_object
muro1.name = "Muro_Largo"

# --- Crear Muro 2 (a lo largo del eje Y) ---
loc_x_muro2 = 0
loc_y_muro2 = (largo_muro2 / 2) - (espesor_muro / 2)
loc_z_muro2 = alto_muro / 2
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(loc_x_muro2, loc_y_muro2, loc_z_muro2),
    scale=(espesor_muro, largo_muro2, alto_muro)
)
muro2 = bpy.context.active_object
muro2.name = "Muro_Corto"