import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_x = 3.0
largo_y = 1.8
alto_z = 1.1
profundidad = 0.7

# Crear el lado largo (eje X)
loc_x1 = (largo_x / 2.0) - profundidad / 2.0
loc_y1 = -(largo_y - profundidad) / 2.0
bpy.ops.mesh.primitive_cube_add(
    location=(loc_x1, loc_y1, alto_z / 2.0),
    scale=(largo_x, profundidad, alto_z)
)
brazo_largo = bpy.context.active_object
brazo_largo.name = 'Mostrador_BrazoLargo'

# Crear el lado corto (eje Y)
loc_x2 = -(largo_x - profundidad) / 2.0
loc_y2 = 0
bpy.ops.mesh.primitive_cube_add(
    location=(loc_x2, loc_y2, alto_z / 2.0),
    scale=(profundidad, largo_y, alto_z)
)
brazo_corto = bpy.context.active_object
brazo_corto.name = 'Mostrador_BrazoCorto'