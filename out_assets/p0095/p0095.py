import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho_pared = 4.0
alto_pared = 2.5
espesor_pared = 0.15
ancho_puerta = 0.9
alto_puerta = 2.1

# Crear el objeto que define el hueco de la puerta
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto_puerta / 2),
    scale=(ancho_puerta, espesor_pared * 1.2, alto_puerta)
)
hueco = bpy.context.active_object
hueco.name = 'HuecoPuertaCutter'
hueco.display_type = 'WIRE'

# Crear la pared sólida
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto_pared / 2),
    scale=(ancho_pared, espesor_pared, alto_pared)
)
pared = bpy.context.active_object
pared.name = 'ParedConHueco'

# Aplicar modificador booleano para crear el hueco
mod_bool = pared.modifiers.new(name='BooleanaPuerta', type='BOOLEAN')
mod_bool.operation = 'DIFFERENCE'
mod_bool.object = hueco

# Aplicar el modificador y borrar el objeto de corte
bpy.ops.object.select_all(action='DESELECT')
pared.select_set(True)
bpy.context.view_layer.objects.active = pared
bpy.ops.object.modifier_apply(modifier=mod_bool.name)

bpy.ops.object.select_all(action='DESELECT')
hueco.select_set(True)
bpy.ops.object.delete()