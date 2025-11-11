import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

ancho = 0.4
profundo = 0.4
alto = 3.0

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto / 2),
    scale=(ancho, profundo, alto)
)

obj = bpy.context.active_object
obj.name = 'ColumnaCuadrada'