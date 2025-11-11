import bpy

bpy.ops.wm.read_homefile(use_empty=True)

scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

largo = 1.2
ancho = 0.5
alto = 0.6
grosor = 0.05

# Crear el volumen exterior
bpy.ops.mesh.primitive_cube_add(
    size=1, 
    location=(0, 0, alto / 2), 
    scale=(largo, ancho, alto)
)
ext_box = bpy.context.active_object
ext_box.name = 'JardineraExterior'

# Crear el volumen interior para el hueco
bpy.ops.mesh.primitive_cube_add(
    size=1, 
    location=(0, 0, alto / 2), 
    scale=(largo - 2 * grosor, ancho - 2 * grosor, alto)
)
int_box = bpy.context.active_object
int_box.name = 'JardineraHueco'
int_box.display_type = 'WIRE'

# Aplicar modificador booleano
bool_mod = ext_box.modifiers.new(name='Boolean', type='BOOLEAN')
bool_mod.operation = 'DIFFERENCE'
bool_mod.object = int_box

bpy.context.view_layer.objects.active = ext_box
bpy.ops.object.modifier_apply(modifier=bool_mod.name)

# Eliminar el objeto de corte
bpy.data.objects.remove(int_box, do_unlink=True)

ext_box.name = 'JardineraDeHormigon'