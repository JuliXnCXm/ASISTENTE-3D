import blender_arch as A
import bpy
from math import pi

A.limpiar_escena()

# --- Entorno de la oficina ---
A.crear_muro('Pared_A', largo=4, alto=2.8, origen=(0,0,0), material='Estuco')
A.crear_muro('Pared_B', largo=3, alto=2.8, origen=(0,0,0), rotacion_z=90, material='Estuco')
A.crear_piso('SueloOficina', ancho=4, fondo=3, material='Parquet')

# --- Mobiliario estándar ---
silla = A.crear_silla('SillaOficina', origen=(1.5, 1.5, 0), material='Cuero')
silla.rotation_euler[2] = pi * 0.75

# --- Escritorio en L (bpy) ---
# Parte larga
bpy.ops.mesh.primitive_cube_add(location=(2, 0.35, 0.725), scale=(1.8, 0.35, 0.025))
parte1 = bpy.context.active_object
# Parte corta
bpy.ops.mesh.primitive_cube_add(location=(0.35, 1.0, 0.725), scale=(0.35, 0.7, 0.025))
parte2 = bpy.context.active_object

# Unir partes
parte1.select_set(True)
parte2.select_set(True)
bpy.context.view_layer.objects.active = parte1
bpy.ops.object.join()
escritorio = bpy.context.active_object
escritorio.name = 'Escritorio_L'
A.asignar_material(escritorio, 'Madera_Roble')

# --- Estantería paramétrica de pared (bpy con modificadores) ---
# Elemento base vertical
bpy.ops.mesh.primitive_cube_add(location=(3.8, 1.0, 1.4), scale=(0.02, 0.2, 1.2))
vertical = bpy.context.active_object
vertical.name = 'Vertical_Base'
A.asignar_material(vertical, 'Marco_Negro')

# Modificador Array para repetir
array_mod = vertical.modifiers.new(name='ArrayVertical', type='ARRAY')
array_mod.count = 15
array_mod.relative_offset_displace[0] = 0
array_mod.relative_offset_displace[1] = -8

# Objeto Empty para controlar la deformación
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(3.8, 1.5, 1.4))
controlador = bpy.context.active_object
controlador.name = 'Controlador_Twist'

# Modificador Simple Deform (Twist)
twist_mod = vertical.modifiers.new(name='TwistParametrico', type='SIMPLE_DEFORM')
twist_mod.deform_method = 'TWIST'
twist_mod.origin = controlador
twist_mod.angle = pi / 2 # 90 grados de torsión
twist_mod.deform_axis = 'Z'

# Estantes horizontales
for z_pos in [1.0, 1.5, 2.0]:
    bpy.ops.mesh.primitive_cube_add(location=(3.8, 1.5, z_pos), scale=(0.02, 1.4, 0.02))
    estante = bpy.context.active_object
    estante.name = f'Estante_H_{z_pos}'
    A.asignar_material(estante, 'Madera_Roble')

A.crear_camara('CamaraOficina', ubicacion=(-1, 4.5, 2), rotacion=(70, 0, -30))