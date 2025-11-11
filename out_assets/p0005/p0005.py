import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
altura_total = 3.0
radio_base = 0.15 / 2
altura_base = 0.04
largo_cable = 0.8
radio_pantalla = 0.4 / 2
altura_pantalla = 0.25

# Base en el techo
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_base,
    depth=altura_base,
    location=(0, 0, altura_total)
)

# Cable
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.005,
    depth=largo_cable,
    location=(0, 0, altura_total - altura_base/2 - largo_cable/2)
)

# Pantalla cónica
bpy.ops.mesh.primitive_cone_add(
    radius1=radio_pantalla,
    radius2=0.05,
    depth=altura_pantalla,
    location=(0, 0, altura_total - altura_base - largo_cable - altura_pantalla/2)
)