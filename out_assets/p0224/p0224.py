import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crear la losa base
bpy.ops.mesh.primitive_cube_add(location=(0, 0, -0.15))
losa = bpy.context.active_object
losa.name = "LosaDeHormigon"
losa.dimensions = (10, 10, 0.3)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Crear el cilindro para el corte
diametro_apertura = 2.0
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_apertura / 2,
    depth=0.5, # Un poco más grueso que la losa para asegurar el corte
    location=(0, 0, 0)
)
cilindro_corte = bpy.context.active_object
cilindro_corte.name = "CilindroDeCorte"
cilindro_corte.display_type = 'WIRE' # Hacerlo visible como alambre para ver el resultado

# Aplicar modificador booleano
mod_bool = losa.modifiers.new(name="CorteCircular", type='BOOLEAN')
mod_bool.operation = 'DIFFERENCE'
mod_bool.object = cilindro_corte

# Opcional: ocultar el cilindro de la vista y el render
cilindro_corte.hide_set(True)
cilindro_corte.hide_render = True