import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar escena
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones generales
largo_banco = 2.0
alto_asiento = 0.45
ancho_asiento = 0.5
grosor_liston = 0.05
espacio_liston = 0.02
num_listones = 6

# Crear soportes de hormigón
ancho_soporte = 0.4
grosor_soporte = 0.1
alto_soporte = 0.4
pos_soportes = largo_banco / 2 - 0.2

bpy.ops.mesh.primitive_cube_add(location=(-pos_soportes, 0, alto_soporte/2))
soporte_1 = bpy.context.object
soporte_1.scale = (grosor_soporte/2, ancho_soporte/2, alto_soporte/2)
bpy.ops.object.transform_apply(scale=True)

bpy.ops.mesh.primitive_cube_add(location=(pos_soportes, 0, alto_soporte/2))
soporte_2 = bpy.context.object
soporte_2.scale = (grosor_soporte/2, ancho_soporte/2, alto_soporte/2)
bpy.ops.object.transform_apply(scale=True)

# Crear listones de madera
ancho_total_listones = num_listones * grosor_liston + (num_listones - 1) * espacio_liston
start_y = -ancho_total_listones / 2 + grosor_liston / 2

for i in range(num_listones):
    y_pos = start_y + i * (grosor_liston + espacio_liston)
    bpy.ops.mesh.primitive_cube_add(location=(0, y_pos, alto_asiento + grosor_liston/2))
    liston = bpy.context.object
    liston.scale = (largo_banco/2, grosor_liston/2, grosor_liston/2)
    bpy.ops.object.transform_apply(scale=True)