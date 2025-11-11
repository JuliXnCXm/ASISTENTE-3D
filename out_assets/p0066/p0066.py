import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones Encimera
largo_encimera = 2.0
ancho_encimera = 0.9
alto_total = 0.9
espesor_encimera = 0.04
retranqueo = 0.05

# Crear Encimera
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto_total - espesor_encimera / 2),
    scale=(largo_encimera, ancho_encimera, espesor_encimera)
)
bpy.context.active_object.name = 'Encimera'

# Dimensiones Base
largo_base = largo_encimera - 2 * retranqueo
ancho_base = ancho_encimera - 2 * retranqueo
alto_base = alto_total - espesor_encimera

# Crear Base
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto_base / 2),
    scale=(largo_base, ancho_base, alto_base)
)
bpy.context.active_object.name = 'BaseIsla'