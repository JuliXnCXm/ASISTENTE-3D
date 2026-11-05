import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones fachada
ancho_fachada = 10.0
alto_fachada = 6.0
grosor_fachada = 0.3

# Dimensiones ventanas
num_ventanas_x = 4
num_ventanas_y = 2
ancho_ventana = 1.2
alto_ventana = 1.5
altura_piso_1 = 1.0
altura_piso_2 = 3.8

# Crear el muro de la fachada
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, alto_fachada / 2))
muro_fachada = bpy.context.active_object
muro_fachada.name = 'Muro_Fachada'
muro_fachada.dimensions = (ancho_fachada, grosor_fachada, alto_fachada)
bpy.ops.object.transform_apply(scale=True)

# Crear un objeto de corte para una ventana
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
corte_ventana_base = bpy.context.active_object
corte_ventana_base.name = 'Corte_Ventana_Base'
corte_ventana_base.dimensions = (ancho_ventana, grosor_fachada + 0.1, alto_ventana)
corte_ventana_base.display_type = 'WIRE'

# Crear retícula de cortes usando modificadores de Array
array_x = corte_ventana_base.modifiers.new(name='Array_X', type='ARRAY')
array_x.count = num_ventanas_x
array_x.relative_offset_displace[0] = (ancho_fachada / num_ventanas_x) / ancho_ventana

array_y = corte_ventana_base.modifiers.new(name='Array_Y', type='ARRAY')
array_y.count = num_ventanas_y
array_y.relative_offset_displace[0] = 0
array_y.relative_offset_displace[2] = (altura_piso_2 - altura_piso_1) / alto_ventana

# Posicionar el objeto de corte inicial para centrar la retícula
pos_x_inicial = -ancho_fachada/2 + (ancho_fachada/num_ventanas_x)/2
pos_z_inicial = altura_piso_1 + alto_ventana/2
corte_ventana_base.location = (pos_x_inicial, 0, pos_z_inicial)

# Aplicar booleana al muro
bool_mod = muro_fachada.modifiers.new(name='BooleanVentanas', type='BOOLEAN')
bool_mod.object = corte_ventana_base
bool_mod.operation = 'DIFFERENCE'
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = muro_fachada
muro_fachada.select_set(True)
bpy.ops.object.modifier_apply(modifier=bool_mod.name)

bpy.data.objects.remove(corte_ventana_base, do_unlink=True)

# Opcional: Añadir cristales
espacio_x = ancho_fachada / num_ventanas_x
for j in range(num_ventanas_y):
    loc_z = altura_piso_1 + alto_ventana / 2 + j * (altura_piso_2 - altura_piso_1)
    for i in range(num_ventanas_x):
        loc_x = pos_x_inicial + i * espacio_x
        bpy.ops.mesh.primitive_plane_add(size=1, location=(loc_x, 0, loc_z))
        cristal = bpy.context.active_object
        cristal.name = f'Cristal_{j+1}_{i+1}'
        cristal.dimensions = (ancho_ventana, alto_ventana, 0)
        cristal.rotation_euler[0] = 1.5708 # 90 grados en X
        bpy.ops.object.transform_apply(scale=True, rotation=True)