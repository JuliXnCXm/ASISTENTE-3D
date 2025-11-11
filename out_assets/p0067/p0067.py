import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

ancho_puerta = 0.8
alto_puerta = 2.1
espesor_puerta = 0.04

ancho_marco = 0.05
fondo_marco = 0.1

# Crear Hoja de la Puerta
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(ancho_puerta / 2, 0, alto_puerta / 2),
    scale=(ancho_puerta, espesor_puerta, alto_puerta)
)
bpy.context.active_object.name = 'HojaPuerta'

# Crear Marco
# Dintel (superior)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(ancho_puerta / 2, 0, alto_puerta + ancho_marco / 2),
    scale=(ancho_puerta + 2 * ancho_marco, fondo_marco, ancho_marco)
)
bpy.context.active_object.name = 'DintelMarco'

# Jamba Izquierda
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-ancho_marco / 2, 0, alto_puerta / 2),
    scale=(ancho_marco, fondo_marco, alto_puerta)
)
bpy.context.active_object.name = 'JambaIzquierda'

# Jamba Derecha
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(ancho_puerta + ancho_marco / 2, 0, alto_puerta / 2),
    scale=(ancho_marco, fondo_marco, alto_puerta)
)
bpy.context.active_object.name = 'JambaDerecha'