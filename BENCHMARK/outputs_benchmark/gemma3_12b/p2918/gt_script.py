import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

largo_muro = 10.0
alto_muro = 2.5
espesor_muro = 0.2

ancho_apertura = 3.0
alto_apertura = 2.2 

# Crear el muro principal
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, alto_muro / 2))
muro = bpy.context.active_object
muro.name = 'Muro_Perimetral'
muro.dimensions = (largo_muro, espesor_muro, alto_muro)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Crear el objeto de corte para la apertura
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, alto_apertura / 2))
corte = bpy.context.active_object
corte.name = 'Corte_Puerta'
corte.dimensions = (ancho_apertura, espesor_muro * 1.1, alto_apertura)
corte.display_type = 'WIRE'

# Aplicar modificador booleano
mod_bool = muro.modifiers.new(name='Apertura', type='BOOLEAN')
mod_bool.object = corte
mod_bool.operation = 'DIFFERENCE'

bpy.context.view_layer.objects.active = muro
bpy.ops.object.modifier_apply(modifier=mod_bool.name)

bpy.data.objects.remove(corte)