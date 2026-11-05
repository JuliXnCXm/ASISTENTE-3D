import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA DEL SALÓN ---
A.crear_habitacion(
    nombre='Salon',
    ancho=4.5, fondo=5.5, alto=2.8,
    material_muro='Estuco',
    material_suelo='Parquet'
)

# --- MOBILIARIO ---
sofa = A.crear_sofa('Sofa_Principal', ancho=2.5, origen=(2.25, 1.0, 0))
sofa.rotation_euler[2] = 3.14159 # 180 grados

# Mueble de TV bajo (usando un cubo escalado con bpy)
bpy.ops.mesh.primitive_cube_add(location=(2.25, 5.0, 0.25))
mueble_tv = bpy.context.active_object
mueble_tv.name = 'Mueble_TV'
mueble_tv.dimensions = (3.0, 0.4, 0.5)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
A.asignar_material(mueble_tv, 'Madera_Roble')

# --- PARED DE ACENTO CON LISTONES (bpy) ---
# Crear el primer listón de madera
bpy.ops.mesh.primitive_cube_add(location=(0.75, 5.5 - 0.101, 1.4))
liston_base = bpy.context.active_object
liston_base.name = 'Liston_Madera'
liston_base.dimensions = (0.04, 0.03, 2.8)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
A.asignar_material(liston_base, 'Madera_Nogal')

# Aplicar modificador Array para crear la pared de listones
array_mod = liston_base.modifiers.new(name='ArrayListones', type='ARRAY')
array_mod.count = 40
array_mod.relative_offset_displace[0] = 2.0 # Separación (0 = juntos, 1 = un listón de espacio)
array_mod.relative_offset_displace[1] = 0
array_mod.relative_offset_displace[2] = 0

# --- ILUMINACIÓN Y CÁMARA ---
A.agregar_luz('Luz_General', tipo='AREA', ubicacion=(2.25, 2.75, 2.7), energia=500, color=(1, 0.95, 0.85))

# Añadir luces tipo 'spot' para acentuar la pared de listones
for i, x_pos in enumerate([1.5, 3.0]):
    A.agregar_luz(f'Foco_Acento_{i}', tipo='SPOT', ubicacion=(x_pos, 4.5, 2.7), energia=150)
    luz_spot = bpy.data.objects[f'Foco_Acento_{i}']
    # Apuntar la luz hacia la pared
    track_to = luz_spot.constraints.new(type='TRACK_TO')
    track_to.target = liston_base
    track_to.track_axis = 'TRACK_NEGATIVE_Z'
    track_to.up_axis = 'UP_Y'

A.crear_camara('Camara_Salon', ubicacion=(2.25, -1, 1.5), rotacion=(80, 0, 0))