import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo = 8.0
ancho = 6.0
espesor = 0.20

# Crear la losa usando un cubo escalado
bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(largo / 2, ancho / 2, -espesor / 2)
)
losa = bpy.context.active_object
losa.name = "LosaPiso"
losa.scale = (largo, ancho, espesor)