import bpy

# Configuración inicial
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
largo_muro = 3.0
alto_muro = 2.5
espesor_muro = 0.15
ancho_puerta = 0.9
alto_puerta = 2.1

# Crear el muro principal
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, alto_muro / 2))
muro = bpy.context.active_object
muro.name = 'MuroConVano'
muro.dimensions = (largo_muro, espesor_muro, alto_muro)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Crear el objeto 'cortador' para el vano
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, alto_puerta / 2))
cortador = bpy.context.active_object
cortador.name = 'CutterPuerta'
cortador.dimensions = (ancho_puerta, espesor_muro * 1.2, alto_puerta) # Un poco más grueso para asegurar el corte
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Aplicar modificador booleano
mod = muro.modifiers.new(name='BooleanVano', type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = cortador

# Aplicar el modificador y eliminar el cortador
bpy.context.view_layer.objects.active = muro
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(cortador, do_unlink=True)