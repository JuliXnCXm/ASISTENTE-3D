import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
tamano_panel = 3.0
grosor_base = 0.05
num_casetones = 3
profundidad_caseton = 0.15
grosor_nervio = 0.10
altura_techo = 3.0

# Crear la losa base del techo
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, altura_techo - grosor_base / 2),
    scale=(tamano_panel, tamano_panel, grosor_base)
)
base_techo = bpy.context.active_object
base_techo.name = 'LosaArtesonado'

# Calcular dimensiones del hueco del casetón
tamano_hueco = (tamano_panel - (num_casetones + 1) * grosor_nervio) / num_casetones

# Crear un objeto para sustraer (un casetón)
bpy.ops.mesh.primitive_cube_add(
    location=(0,0,0), # La posición se controla con el array
    scale=(tamano_hueco, tamano_hueco, profundidad_caseton)
)
caseton_cutter = bpy.context.active_object
caseton_cutter.name = 'CasetonCutter'
caseton_cutter.display_type = 'WIRE' # Hacerlo invisible en render, visible como alambre
caseton_cutter.hide_render = True

# Usar modificadores de array para crear la retícula
array_x = caseton_cutter.modifiers.new(name='ArrayX', type='ARRAY')
array_x.count = num_casetones
array_x.relative_offset_displace[0] = 0
array_x.constant_offset_displace[0] = tamano_hueco + grosor_nervio

array_y = caseton_cutter.modifiers.new(name='ArrayY', type='ARRAY')
array_y.count = num_casetones
array_y.relative_offset_displace[0] = 0
array_y.relative_offset_displace[1] = 0
array_y.constant_offset_displace[1] = tamano_hueco + grosor_nervio

# Posicionar la retícula de cortadores
pos_inicial = -tamano_panel/2 + grosor_nervio + tamano_hueco/2
caseton_cutter.location = (
    pos_inicial,
    pos_inicial,
    altura_techo - grosor_base - profundidad_caseton / 2
)

# Aplicar un booleano a la losa base
bool_mod = base_techo.modifiers.new(name='SustraccionCasetones', type='BOOLEAN')
bool_mod.operation = 'DIFFERENCE'
bool_mod.object = caseton_cutter