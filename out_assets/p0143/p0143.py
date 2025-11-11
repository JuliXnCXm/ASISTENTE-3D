import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

muro_largo = 5.0
muro_alto = 2.8
muro_espesor = 0.25
puerta_ancho = 0.9
puerta_alto = 2.1
distancia_borde = 1.0

# Muro
bpy.ops.mesh.primitive_cube_add(
    location=(muro_largo / 2, 0, muro_alto / 2),
    scale=(muro_largo, muro_espesor, muro_alto)
)
muro = bpy.context.active_object
muro.name = "MuroConApertura"

# Hueco
loc_hueco_x = distancia_borde + puerta_ancho / 2
loc_hueco_z = puerta_alto / 2
bpy.ops.mesh.primitive_cube_add(
    location=(loc_hueco_x, 0, loc_hueco_z),
    scale=(puerta_ancho, muro_espesor * 1.1, puerta_alto)
)
hueco = bpy.context.active_object
hueco.name = "HuecoPuerta"

# Booleano
mod = muro.modifiers.new(name='Boolean', type='BOOLEAN')
mod.object = hueco
mod.operation = 'DIFFERENCE'

bpy.context.view_layer.objects.active = muro
muro.select_set(True)
bpy.ops.object.modifier_apply(modifier=mod.name)

bpy.data.objects.remove(hueco, do_unlink=True)
