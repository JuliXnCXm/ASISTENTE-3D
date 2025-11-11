import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones de la losa
largo = 6.0
ancho = 4.0
espesor = 0.20

# Creación de la losa (usando un cubo)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(largo / 2, ancho / 2, -espesor / 2),
    scale=(largo, ancho, espesor)
)

losa = bpy.context.active_object
losa.name = "LosaPiso"