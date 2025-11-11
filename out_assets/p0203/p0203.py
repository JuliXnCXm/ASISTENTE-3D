import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar escena
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo = 5.0
alto = 3.0
espesor = 0.2

# Crear primer muro (a lo largo del eje Y)
bpy.ops.mesh.primitive_cube_add(
    location=(espesor / 2, largo / 2, alto / 2)
)
muro_1 = bpy.context.object
muro_1.scale = (espesor / 2, largo / 2, alto / 2)
bpy.ops.object.transform_apply(scale=True)
muro_1.name = "Muro_Norte"

# Crear segundo muro (a lo largo del eje X)
bpy.ops.mesh.primitive_cube_add(
    location=(largo / 2, espesor / 2, alto / 2)
)
muro_2 = bpy.context.object
muro_2.scale = (largo / 2, espesor / 2, alto / 2)
bpy.ops.object.transform_apply(scale=True)
muro_2.name = "Muro_Oeste"