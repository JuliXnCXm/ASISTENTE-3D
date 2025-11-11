import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar escena
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
diametro = 15.0
espesor = 0.3

# Crear la losa circular
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro / 2,
    depth=espesor,
    location=(0, 0, espesor / 2),
    vertices=128
)
losa = bpy.context.object
losa.name = "Losa_Plaza"