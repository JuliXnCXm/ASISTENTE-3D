import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

largo = 2.0
ancho = 0.5
alto = 0.6
grosor = 0.05

# Volumen exterior
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, alto / 2),
    scale=(largo / 2, ancho / 2, alto / 2)
)
exterior = bpy.context.active_object
exterior.name = "JardineraExterior"

# Volumen interior para vaciar
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, alto / 2),
    scale=((largo - 2 * grosor) / 2, (ancho - 2 * grosor) / 2, alto / 2)
)
interior = bpy.context.active_object
interior.name = "JardineraVaciado"
interior.location.z = alto  # apartar visualmente

mod = exterior.modifiers.new(name='Boolean', type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = interior

bpy.context.view_layer.objects.active = exterior
exterior.select_set(True)
bpy.ops.object.modifier_apply(modifier=mod.name)

bpy.data.objects.remove(interior, do_unlink=True)

# Fondo
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, grosor / 2),
    scale=((largo - 2 * grosor) / 2, (ancho - 2 * grosor) / 2, grosor / 2)
)
fondo = bpy.context.active_object
fondo.name = "JardineraFondo"

# Unir
bpy.ops.object.select_all(action='DESELECT')
exterior.select_set(True)
fondo.select_set(True)
bpy.context.view_layer.objects.active = exterior
bpy.ops.object.join()
