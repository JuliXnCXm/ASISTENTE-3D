import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

largo = 5.0
ancho = 4.0
altura_techo = 2.5
ancho_rebaje = 0.2
alto_rebaje = 0.1
espesor_techo = 0.02

# Crear la parte central (más baja)
largo_central = largo - 2 * ancho_rebaje
ancho_central = ancho - 2 * ancho_rebaje
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, altura_techo - alto_rebaje - espesor_techo/2),
    scale=(largo_central, ancho_central, espesor_techo)
)
bpy.context.active_object.name = 'TechoCentral'

# Crear el perímetro (más alto)
# Usar un cubo grande, restar el interior con un booleano
# Cubo exterior
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, altura_techo - espesor_techo/2),
    scale=(largo, ancho, espesor_techo)
)
perimetro = bpy.context.active_object
perimetro.name = 'TechoPerimetral'

# Cubo interior para cortar
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, altura_techo - espesor_techo/2),
    scale=(largo_central, ancho_central, espesor_techo * 4) # Más grueso para asegurar corte
)
cortador = bpy.context.active_object
cortador.name = 'CortadorBooleano'

# Aplicar modificador booleano
mod = perimetro.modifiers.new(name='Boolean', type='BOOLEAN')
mod.object = cortador
mod.operation = 'DIFFERENCE'
bpy.context.view_layer.objects.active = perimetro
bpy.ops.object.modifier_apply(modifier=mod.name)

# Eliminar el cortador
bpy.data.objects.remove(cortador, do_unlink=True)