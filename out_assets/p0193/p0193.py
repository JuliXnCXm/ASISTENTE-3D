import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

largo = 3.0
ancho = 0.8
alto = 0.6
grosor = 0.1

# Crear el volumen exterior
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, alto / 2),
    scale=(largo / 2, ancho / 2, alto / 2)
)
exterior_obj = bpy.context.active_object
exterior_obj.name = "Jardinera_Exterior"

# Crear el volumen interior para el hueco
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, alto / 2),
    scale=((largo - 2 * grosor) / 2, (ancho - 2 * grosor) / 2, alto / 2)
)
interior_obj = bpy.context.active_object
interior_obj.name = "Jardinera_Interior_Cutter"
interior_obj.display_type = 'WIRE'

# Aplicar modificador booleano
mod = exterior_obj.modifiers.new(name='BooleanHole', type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = interior_obj

bpy.context.view_layer.objects.active = exterior_obj
bpy.ops.object.modifier_apply(modifier=mod.name)

# Eliminar el objeto de corte
bpy.data.objects.remove(interior_obj, do_unlink=True)

exterior_obj.name = "JardineraHormigon"