import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_isla = 2.0
ancho_isla = 0.9
alto_isla = 0.95
voladizo = 0.3
espesor_encimera = 0.04

# Crear el cuerpo base de la isla
ancho_base = ancho_isla - voladizo
alto_base = alto_isla - espesor_encimera

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, voladizo / 2, alto_base / 2),
    scale=(largo_isla, ancho_base, alto_base)
)
base = bpy.context.active_object
base.name = 'BaseIsla'

# Crear la encimera
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto_isla - espesor_encimera / 2),
    scale=(largo_isla, ancho_isla, espesor_encimera)
)
encimera = bpy.context.active_object
encimera.name = 'EncimeraIsla'