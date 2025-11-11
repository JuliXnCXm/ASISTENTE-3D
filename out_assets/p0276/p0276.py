import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
tamano_losa = 5.0
espesor_losa = 0.2
diametro_hueco = 1.0

# --- Crear la losa base ---
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, -espesor_losa / 2),
    scale=(tamano_losa, tamano_losa, espesor_losa)
)
losa = bpy.context.active_object
losa.name = "LosaHormigon"

# --- Crear el cilindro para el hueco ---
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_hueco / 2,
    depth=espesor_losa * 2, # Asegura que atraviese completamente
    location=(0, 0, 0)
)
cilindro_corte = bpy.context.active_object
cilindro_corte.name = "CilindroCorte"

# --- Configurar el modificador booleano (sin aplicarlo) ---
mod = losa.modifiers.new(name='BooleanHole', type='BOOLEAN')
mod.object = cilindro_corte
mod.operation = 'DIFFERENCE'

# --- Ocultar el cilindro para que solo se vea el resultado ---
cilindro_corte.display_type = 'WIRE'
cilindro_corte.hide_render = True