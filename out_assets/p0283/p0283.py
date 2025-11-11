import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones fachada
fachada_ancho = 7.0
fachada_alto = 4.0
fachada_espesor = 0.3

# Dimensiones ventana
ventana_ancho = 1.5
ventana_alto = 1.5
altura_suelo_ventana = 1.0

# Crear el muro de la fachada
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, fachada_alto / 2),
    scale=(fachada_ancho, fachada_espesor, fachada_alto)
)
muro_fachada = bpy.context.active_object
muro_fachada.name = 'MuroFachada'

# Crear el objeto para el hueco (booleana)
loc_z_ventana = altura_suelo_ventana + (ventana_alto / 2)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, loc_z_ventana),
    scale=(ventana_ancho, fachada_espesor * 1.1, ventana_alto)
)
hueco = bpy.context.active_object
hueco.name = 'HuecoVentana'

# Aplicar modificador booleano
bool_mod = muro_fachada.modifiers.new(name='BooleanVentana', type='BOOLEAN')
bool_mod.object = hueco
bool_mod.operation = 'DIFFERENCE'

bpy.ops.object.select_all(action='DESELECT')
muro_fachada.select_set(True)
bpy.context.view_layer.objects.active = muro_fachada
bpy.ops.object.modifier_apply(modifier=bool_mod.name)

# Eliminar el objeto del hueco
bpy.data.objects.remove(hueco)