import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones del muro
largo = 4.0
alto = 2.5
espesor = 0.15

# Crear el muro usando un cubo primitivo
bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(largo / 2, espesor / 2, alto / 2)
)

# Escalar el cubo a las dimensiones deseadas
muro = bpy.context.active_object
muro.name = 'MuroInterior'
muro.scale = (largo / 2, espesor / 2, alto / 2)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)