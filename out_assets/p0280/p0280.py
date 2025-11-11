import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones de la losa
ancho = 5.0  # metros
largo = 5.0  # metros
espesor = 0.20 # metros (20 cm)

# Crear la losa usando un cubo
bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(0, 0, espesor / 2)
)

# Ajustar dimensiones del objeto recién creado
losa = bpy.context.active_object
losa.name = 'LosaHormigon'
losa.dimensions = (ancho, largo, espesor)