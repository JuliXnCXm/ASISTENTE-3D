import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
profundidad = 0.6
altura = 0.9
grosor = 0.05
largo_central = 3.0
largo_lateral = 2.0

# Tramo central (a lo largo de X)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_central / 2, profundidad / 2, altura - grosor / 2),
    scale=(largo_central, profundidad, grosor)
)

# Tramo lateral izquierdo (a lo largo de Y)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(profundidad / 2, profundidad + (largo_lateral - profundidad)/2, altura - grosor / 2),
    scale=(profundidad, largo_lateral - profundidad, grosor)
)

# Tramo lateral derecho (a lo largo de Y)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_central - profundidad / 2, profundidad + (largo_lateral - profundidad)/2, altura - grosor / 2),
    scale=(profundidad, largo_lateral - profundidad, grosor)
)