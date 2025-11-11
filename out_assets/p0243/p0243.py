import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_banco = 2.0
ancho_banco = 0.4
altura_total = 0.45
grosor_asiento = 0.05
ancho_soporte = 0.3

# Crear asiento
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, altura_total - grosor_asiento / 2),
    scale=(largo_banco, ancho_banco, grosor_asiento)
)
bpy.context.object.name = 'Asiento_Banco'

# Crear soportes
altura_soporte = altura_total - grosor_asiento
pos_x_soporte = (largo_banco / 2) - (ancho_soporte / 2)

# Soporte 1
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-pos_x_soporte, 0, altura_soporte / 2),
    scale=(ancho_soporte, ancho_banco, altura_soporte)
)
bpy.context.object.name = 'Soporte_Izquierdo'

# Soporte 2
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(pos_x_soporte, 0, altura_soporte / 2),
    scale=(ancho_soporte, ancho_banco, altura_soporte)
)
bpy.context.object.name = 'Soporte_Derecho'