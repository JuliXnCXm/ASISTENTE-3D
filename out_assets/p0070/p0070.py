import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
alto = 2.8
espesor = 0.15
largo_norte_x = 5.0
largo_oeste_y = 4.0

# Crear Muro Norte (a lo largo del eje X)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, (largo_oeste_y - espesor) / 2.0, alto / 2.0),
    scale=(largo_norte_x, espesor, alto)
)
muro_norte = bpy.context.active_object
muro_norte.name = 'MuroNorte'

# Crear Muro Oeste (a lo largo del eje Y)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-(largo_norte_x - espesor) / 2.0, 0, alto / 2.0),
    scale=(espesor, largo_oeste_y, alto)
)
muro_oeste = bpy.context.active_object
muro_oeste.name = 'MuroOeste'