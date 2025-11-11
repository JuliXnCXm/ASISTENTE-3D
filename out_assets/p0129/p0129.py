import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
alto = 2.7
espesor = 0.15
largo1 = 5.0
largo2 = 3.0

# Crear Muro 1 (a lo largo del eje X)
bpy.ops.mesh.primitive_cube_add(size=1)
muro1 = bpy.context.object
muro1.name = "Muro_Largo"
muro1.dimensions = (largo1, espesor, alto)
muro1.location = (largo1 / 2, -espesor / 2, alto / 2)

# Crear Muro 2 (a lo largo del eje Y)
bpy.ops.mesh.primitive_cube_add(size=1)
muro2 = bpy.context.object
muro2.name = "Muro_Corto"
muro2.dimensions = (espesor, largo2, alto)
muro2.location = (-espesor / 2, largo2 / 2, alto / 2)