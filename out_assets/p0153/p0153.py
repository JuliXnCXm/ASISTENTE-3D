import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_x = 10.0
largo_y = 8.0
alto = 2.5
espesor = 0.2

# Crear muro en el eje X
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_x / 2, espesor / 2, alto / 2),
    scale=(largo_x, espesor, alto)
)
muro_x = bpy.context.active_object
muro_x.name = "MuroPerimetral_X"

# Crear muro en el eje Y
# Se ajusta la longitud y posición para que encaje en la esquina sin superponerse
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(espesor / 2, (largo_y + espesor) / 2, alto / 2),
    scale=(espesor, largo_y - espesor, alto)
)
muro_y = bpy.context.active_object
muro_y.name = "MuroPerimetral_Y"