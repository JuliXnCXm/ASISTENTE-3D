import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA DE LA HABITACIÓN ---
habitacion = A.crear_habitacion(
    'SalaEstar',
    ancho=6, fondo=5, alto=3.0,
    material_muro='Estuco',
    material_suelo='Parquet'
)

# --- SOFÁ MODULAR (usando blender_arch y bpy) ---
sofa_principal = A.crear_sofa(
    'Sofa_Principal', ancho=2.5, fondo=1.0, alto_asiento=0.45,
    origen=(-1.25, -2.0, 0), material='Tela_Gris'
)

# Módulo chaise longue con bpy
bpy.ops.mesh.primitive_cube_add(location=(1.0, -1.25, 0.225))
chaise = bpy.context.active_object
chaise.name = 'Sofa_Chaise'
chaise.scale = (1.5, 1.0, 0.45)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
A.asignar_material(chaise, nombre='Tela_Gris')

# --- ESTANTERÍA DE DISEÑO (usando bpy y modificadores) ---
# Base vertical
bpy.ops.mesh.primitive_cube_add(location=(-2.9, 0, 1.5))
base_estanteria = bpy.context.active_object
base_estanteria.name = 'Base_Estanteria'
base_estanteria.scale = (0.05, 1.5, 3.0)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
A.asignar_material(base_estanteria, nombre='Madera_Roble')

# Modificador Array para las verticales
mod_array_v = base_estanteria.modifiers.new(name='ArrayVertical', type='ARRAY')
mod_array_v.count = 4
mod_array_v.relative_offset_displace[0] = 0
mod_array_v.relative_offset_displace[2] = 0
mod_array_v.use_relative_offset = False
mod_array_v.use_constant_offset = True
mod_array_v.constant_offset_displace[1] = 1.0

# Estantes horizontales irregulares
estantes_pos = [
    (0.5, 0.4), (1.0, 0.8), (0.2, 1.2), (1.8, 1.5),
    (2.5, 1.8), (1.2, 2.2), (0.8, 2.6)
]
for i, (largo, altura) in enumerate(estantes_pos):
    bpy.ops.mesh.primitive_cube_add(location=(-2.9, -1.0 + largo/2, altura))
    estante = bpy.context.active_object
    estante.name = f'Estante_{i}'
    estante.scale = (0.05, largo, 0.05)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    A.asignar_material(estante, nombre='Madera_Roble')

# --- ALFOMBRA (usando bpy) ---
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -0.5, 0.01))
alfombra = bpy.context.active_object
alfombra.name = 'Alfombra'
alfombra.scale = (3.5, 3.0, 1)
A.asignar_material(alfombra, nombre='Alfombra_Lana', base_color=(0.8, 0.7, 0.6, 1))

# Solidificar la alfombra
mod_solidify = alfombra.modifiers.new(name='Grosor', type='SOLIDIFY')
mod_solidify.thickness = 0.02

# --- ILUMINACIÓN Y CÁMARA ---
A.agregar_luz('Luz_Principal', tipo='AREA', ubicacion=(0, 0, 2.8), energia=250, color=(1, 0.95, 0.85))
A.crear_camara('CamaraSala', ubicacion=(5, 2, 1.8), rotacion=(80, 0, 110))