import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

largo_norte = 6.0
largo_este = 4.0
alto = 2.8
espesor = 0.25

# Muro Norte (a lo largo del eje Y)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(espesor / 2, largo_norte / 2, alto / 2),
    scale=(espesor, largo_norte, alto)
)
muro_norte = bpy.context.active_object
muro_norte.name = "MuroNorte"

# Muro Este (a lo largo del eje X)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=((largo_este + espesor) / 2, espesor / 2, alto / 2),
    scale=(largo_este - espesor, espesor, alto)
)
muro_este = bpy.context.active_object
muro_este.name = "MuroEste"