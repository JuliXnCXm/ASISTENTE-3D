import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones de la losa
largo = 5.0
ancho = 5.0
espesor = 0.20

# La ubicación en Z se ajusta para que la cara superior esté en Z=0
loc_z = -espesor / 2

# Creación de la losa
bpy.ops.mesh.primitive_cube_add(
    size=1,
    scale=(largo, ancho, espesor),
    location=(0, 0, loc_z)
)