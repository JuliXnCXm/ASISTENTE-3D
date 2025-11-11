import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones de la habitación y techo
room_x, room_y, room_z = 6.0, 4.0, 3.0

# Dimensiones del casetón (hueco + nervio)
tile_size = 1.0
nervio_ancho = 0.1
hueco_profundidad = 0.2

# Crear la losa base del techo
bpy.ops.mesh.primitive_cube_add(
    location=(room_x / 2, room_y / 2, room_z - 0.05),
    scale=(room_x, room_y, 0.1)
)
techo_base = bpy.context.active_object
techo_base.name = 'LosaTecho'

# Crear el objeto 'cortador' que definirá un hueco
hueco_size = tile_size - nervio_ancho
bpy.ops.mesh.primitive_cube_add(
    location=(tile_size / 2, tile_size / 2, room_z - hueco_profundidad / 2),
    scale=(hueco_size, hueco_size, hueco_profundidad)
)
cortador = bpy.context.active_object
cortador.name = 'Cutter'
cortador.display_type = 'WIRE' # Hacerlo visible pero no sólido

# Usar Array modifiers para crear la retícula de cortadores
mod_array_x = cortador.modifiers.new(name='Array_X', type='ARRAY')
mod_array_x.count = int(room_x / tile_size)
mod_array_x.relative_offset_displace[0] = tile_size / hueco_size
mod_array_x.relative_offset_displace[1] = 0

mod_array_y = cortador.modifiers.new(name='Array_Y', type='ARRAY')
mod_array_y.count = int(room_y / tile_size)
mod_array_y.relative_offset_displace[0] = 0
mod_array_y.relative_offset_displace[1] = tile_size / hueco_size

# Aplicar una operación booleana para crear los huecos
mod_bool = techo_base.modifiers.new(name='BooleanaCaseton', type='BOOLEAN')
mod_bool.object = cortador
mod_bool.operation = 'DIFFERENCE'

# Opcional: Aplicar modificadores y limpiar
# bpy.context.view_layer.objects.active = techo_base
# bpy.ops.object.modifier_apply(modifier=mod_bool.name)
# bpy.data.objects.remove(cortador)