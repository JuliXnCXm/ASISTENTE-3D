import bpy

bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_banco = 2.0
ancho_banco = 0.45
alto_asiento = 0.45

# Soportes de hormigón
ancho_soporte = 0.1
alto_soporte = 0.4
pos_soportes = (largo_banco / 2) - (ancho_soporte / 2) - 0.1

bpy.ops.mesh.primitive_cube_add(size=1, location=(-pos_soportes, 0, alto_soporte/2), scale=(ancho_soporte, ancho_banco, alto_soporte))
bpy.context.object.name = 'Soporte_Izquierdo'
bpy.ops.mesh.primitive_cube_add(size=1, location=(pos_soportes, 0, alto_soporte/2), scale=(ancho_soporte, ancho_banco, alto_soporte))
bpy.context.object.name = 'Soporte_Derecho'

# Listones de madera
num_listones = 3
ancho_liston = 0.1
espesor_liston = 0.05
espacio_listones = (ancho_banco - num_listones * ancho_liston) / (num_listones - 1)

for i in range(num_listones):
    pos_y = -ancho_banco / 2 + ancho_liston / 2 + i * (ancho_liston + espacio_listones)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, pos_y, alto_asiento + espesor_liston / 2),
        scale=(largo_banco, ancho_liston, espesor_liston)
    )
    bpy.context.object.name = f'Liston_{i+1}'