import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_sur = 5.0
largo_oeste = 4.0
altura = 2.7
grosor = 0.2

# Crear muro sur (a lo largo del eje X)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_sur / 2, -grosor / 2, altura / 2),
    scale=(largo_sur, grosor, altura)
)
bpy.context.object.name = 'Muro_Sur'

# Crear muro oeste (a lo largo del eje Y)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-grosor / 2, largo_oeste / 2, altura / 2),
    scale=(grosor, largo_oeste, altura)
)
bpy.context.object.name = 'Muro_Oeste'