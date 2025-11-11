import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo1 = 8.0
largo2 = 6.0
alto = 2.0
espesor = 0.4

# Crear primer tramo del muro (a lo largo del eje X)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo1 / 2, -espesor / 2, alto / 2)
)
tramo1 = bpy.context.active_object
tramo1.name = "Muro_L_Tramo1"
tramo1.dimensions = (largo1, espesor, alto)

# Crear segundo tramo del muro (a lo largo del eje Y)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-espesor / 2, largo2 / 2, alto / 2)
)
tramo2 = bpy.context.active_object
tramo2.name = "Muro_L_Tramo2"
tramo2.dimensions = (espesor, largo2, alto)