import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho_exterior = 0.50
alto_exterior = 0.70
grosor_marco = 0.03
profundidad_marco = 0.04
ancho_paspartu = 0.05

# Crear un muro de fondo para colgar el cuadro
bpy.ops.mesh.primitive_cube_add(
    location=(0, -0.075, 1.25),
    scale=(2.0, 0.15, 2.5)
)
bpy.context.active_object.name = 'MuroSoporte'

# Crear la base del marco
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, 1.5),
    scale=(ancho_exterior, profundidad_marco, alto_exterior)
)
marco_base = bpy.context.active_object
marco_base.name = 'Marco'
marco_base.rotation_euler[0] = 1.5708 # 90 grados en X para ponerlo vertical

# Crear el objeto para cortar el interior (hueco del paspartú)
ancho_corte_paspartu = ancho_exterior - 2 * grosor_marco
alto_corte_paspartu = alto_exterior - 2 * grosor_marco
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0.005, 1.5),
    scale=(ancho_corte_paspartu, profundidad_marco, alto_corte_paspartu)
)
cortador1 = bpy.context.active_object
cortador1.rotation_euler[0] = 1.5708

# Crear el objeto para el rebaje del lienzo/foto
ancho_corte_lienzo = ancho_corte_paspartu - 2 * ancho_paspartu
alto_corte_lienzo = alto_corte_paspartu - 2 * ancho_paspartu
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0.02, 1.5),
    scale=(ancho_corte_lienzo, profundidad_marco / 2, alto_corte_lienzo)
)
cortador2 = bpy.context.active_object
cortador2.rotation_euler[0] = 1.5708

# Aplicar booleanos
bool1 = marco_base.modifiers.new(name='CorteInterior', type='BOOLEAN')
bool1.operation = 'DIFFERENCE'
bool1.object = cortador1
bpy.ops.object.modifier_apply(modifier=bool1.name)

bool2 = marco_base.modifiers.new(name='CorteLienzo', type='BOOLEAN')
bool2.operation = 'DIFFERENCE'
bool2.object = cortador2
bpy.ops.object.modifier_apply(modifier=bool2.name)

# Limpiar objetos cortadores
bpy.data.objects.remove(cortador1)
bpy.data.objects.remove(cortador2)