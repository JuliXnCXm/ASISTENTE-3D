import blender_arch as A
import bpy
from math import pi

A.limpiar_escena()

# --- Estructura de la caja de escalera ---
muro_anclaje = A.crear_muro('Muro_Anclaje', largo=4, alto=5.6, grosor=0.2, origen=(0, 0, 0), material='Hormigon')
muro_frente = A.crear_muro('Muro_Frente', largo=1.5, alto=5.6, grosor=0.2, origen=(0, 1.3, 0), rotacion_z=90, material='Hormigon')
losa_inf = A.crear_losa_rectangular('Losa_Inferior', ancho=4, fondo=1.5, espesor=0.2, origen=(0, 0, -0.2), material='Hormigon')
losa_sup = A.crear_losa_rectangular('Losa_Superior', ancho=2.5, fondo=1.5, espesor=0.2, origen=(1.5, 0, 2.6), material='Hormigon')

# --- Peldaños Flotantes (bpy con Array modifier) ---
num_peldanos = 15
huella = 0.28
contrahuella = 0.18
ancho_peldano = 1.0
grosor_peldano = 0.08

# Crear el primer peldaño
bpy.ops.mesh.primitive_cube_add(location=(huella/2, ancho_peldano/2, contrahuella - grosor_peldano/2), scale=(huella, ancho_peldano, grosor_peldano))
peldano_base = bpy.context.active_object
peldano_base.name = 'Peldano_01'
A.asignar_material(peldano_base, nombre='Madera_Nogal')

# Modificador Array para crear la escalera
array_mod = peldano_base.modifiers.new(name='ArrayEscalera', type='ARRAY')
array_mod.count = num_peldanos
array_mod.use_relative_offset = False
array_mod.use_constant_offset = True
array_mod.constant_offset_displace = (huella, 0, contrahuella)

# --- Baranda de Vidrio y Pasamanos (bpy) ---
# Paneles de vidrio
for i in range(4):
    x_pos = 0.3 + i * 1.0
    z_pos = 0.9 + i * 1.0 * (contrahuella/huella)
    bpy.ops.mesh.primitive_plane_add(location=(x_pos, 1.0, z_pos))
    panel = bpy.context.active_object
    panel.name = f'Panel_Vidrio_{i}'
    panel.scale = (0.9, 0.9, 1)
    panel.rotation_euler[0] = pi/2
    panel.rotation_euler[2] = 0.5585 # Angulo de la escalera atan(0.18/0.28)
    solid_mod = panel.modifiers.new(name='Grosor', type='SOLIDIFY')
    solid_mod.thickness = 0.015
    A.asignar_material(panel, nombre='Vidrio_Templado')

# Pasamanos
bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=4.2, location=(2.0, 1.0, 1.8))
pasamanos = bpy.context.active_object
pasamanos.name = 'Pasamanos'
pasamanos.rotation_euler[1] = 0.5585
A.asignar_material(pasamanos, nombre='Acero_Inox')

A.agregar_luz('Luz_Escalera', tipo='SPOT', ubicacion=(2, 0.5, 5), energia=2000)
A.crear_camara('Camara', ubicacion=(5, -2, 2.5), rotacion=(80, 0, 60))