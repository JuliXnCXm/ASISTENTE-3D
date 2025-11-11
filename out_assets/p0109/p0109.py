import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo = 3.0
alto = 2.5
espesor = 0.2

# Crear Muro 1 (en el eje X)
bpy.ops.mesh.primitive_cube_add(
    location=(largo / 2, espesor / 2, alto / 2),
    scale=(largo, espesor, alto)
)

# Crear Muro 2 (en el eje Y)
# Se ajusta la longitud y posición para que encaje en la esquina interior
largo_muro2 = largo - espesor
loc_x_muro2 = espesor / 2
loc_y_muro2 = espesor + (largo_muro2 / 2)
bpy.ops.mesh.primitive_cube_add(
    location=(loc_x_muro2, loc_y_muro2, alto / 2),
    scale=(espesor, largo_muro2, alto)
)