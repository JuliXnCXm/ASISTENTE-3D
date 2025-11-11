import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones del muro
muro_largo = 4.0
muro_alto = 2.5
muro_espesor = 0.3

# Dimensiones del nicho
nicho_ancho = 1.0
nicho_alto = 1.5
nicho_prof = 0.2

# Crear muro principal
bpy.ops.mesh.primitive_cube_add(
    size=1, 
    location=(0, 0, muro_alto / 2), 
    scale=(muro_largo, muro_espesor, muro_alto)
)
muro = bpy.context.active_object
muro.name = "MuroConNicho"

# Crear el objeto que cortará el nicho (booleano)
# Se hace ligeramente más profundo para asegurar un corte limpio
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, -muro_espesor/2 + nicho_prof/2 - 0.01, 1.25), # Centrado en altura
    scale=(nicho_ancho, nicho_prof + 0.02, nicho_alto)
)
cortador = bpy.context.active_object
cortador.name = "CortadorNicho"
cortador.display_type = 'WIRE'

# Aplicar modificador booleano
bool_mod = muro.modifiers.new(name='NichoBooleano', type='BOOLEAN')
bool_mod.object = cortador
bool_mod.operation = 'DIFFERENCE'

bpy.context.view_layer.objects.active = muro
muro.select_set(True)
bpy.ops.object.modifier_apply(modifier=bool_mod.name)

# Eliminar el objeto cortador
bpy.data.objects.remove(cortador, do_unlink=True)