import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

diametro_tablero = 0.90
espesor_tablero = 0.04
altura_base = 0.35
diametro_base = 0.40

altura_total = altura_base + espesor_tablero

# Tablero
bpy.ops.mesh.primitive_cylinder_add(
    vertices=64,
    radius=diametro_tablero / 2,
    depth=espesor_tablero,
    location=(0, 0, altura_base + espesor_tablero / 2)
)
tablero = bpy.context.active_object
tablero.name = 'TableroMesa'

# Base
bpy.ops.mesh.primitive_cylinder_add(
    vertices=64,
    radius=diametro_base / 2,
    depth=altura_base,
    location=(0, 0, altura_base / 2)
)
base = bpy.context.active_object
base.name = 'BaseMesa'