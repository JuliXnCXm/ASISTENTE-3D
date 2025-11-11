import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_norte = 5.0
largo_oeste = 4.0
altura = 2.8
espesor = 0.25

# Crear Muro Norte (a lo largo del eje X)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_norte / 2 - espesor / 2, -espesor / 2, altura / 2),
    scale=(largo_norte - espesor, espesor, altura)
)
muro_norte = bpy.context.active_object
muro_norte.name = "MuroNorte"

# Crear Muro Oeste (a lo largo del eje Y)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-espesor / 2, largo_oeste / 2 - espesor / 2, altura / 2),
    scale=(espesor, largo_oeste - espesor, altura)
)
muro_oeste = bpy.context.active_object
muro_oeste.name = "MuroOeste"