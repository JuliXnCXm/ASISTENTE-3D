import blender_arch as A
import bpy

A.limpiar_escena()

# --- Estructura de la habitación ---
habitacion = A.crear_habitacion('Salon', ancho=6, fondo=4.5, alto=2.8, material_muro='Estuco', material_suelo='Parquet')

# --- Mobiliario principal ---
sofa = A.crear_sofa('Sofa_Principal', ancho=3, fondo=1, origen=(1.5, 3.2, 0))
A.asignar_material(sofa, nombre='Tela_Gris')

# --- Mueble de TV flotante (bpy) ---
bpy.ops.mesh.primitive_cube_add(location=(3, 0.25, 0.4))
mueble_tv = bpy.context.active_object
mueble_tv.name = 'Mueble_TV_Flotante'
mueble_tv.dimensions = (2.5, 0.5, 0.3)
A.asignar_material(mueble_tv, nombre='Madera_Nogal')

# --- Estantería de obra con nichos (bpy y booleanos) ---
# Muro base para la estantería
bpy.ops.mesh.primitive_cube_add(location=(0.15, 2.25, 1.4))
muro_estanteria = bpy.context.active_object
muro_estanteria.name = 'Muro_Estanteria'
muro_estanteria.dimensions = (0.3, 4.5, 2.8)
A.asignar_material(muro_estanteria, nombre='Estuco')

# Cortadores para los nichos
nichos_props = [
    {'loc': (0.15, 1, 2.0), 'dims': (0.4, 0.8, 0.8)},
    {'loc': (0.15, 3, 2.2), 'dims': (0.4, 1.2, 0.4)},
    {'loc': (0.15, 2, 0.8), 'dims': (0.4, 1.8, 0.6)}
]

for i, props in enumerate(nichos_props):
    bpy.ops.mesh.primitive_cube_add(location=props['loc'])
    cortador = bpy.context.active_object
    cortador.name = f'Cortador_Nicho_{i}'
    cortador.dimensions = props['dims']
    cortador.display_type = 'WIRE'
    
    # Aplicar modificador booleano al muro
    mod_bool = muro_estanteria.modifiers.new(name=f'Booleana_Nicho_{i}', type='BOOLEAN')
    mod_bool.operation = 'DIFFERENCE'
    mod_bool.object = cortador

# Se recomienda aplicar los modificadores y ocultar los cortadores
# bpy.ops.object.select_all(action='DESELECT')
# muro_estanteria.select_set(True)
# bpy.context.view_layer.objects.active = muro_estanteria
# for mod in muro_estanteria.modifiers:
#     bpy.ops.object.modifier_apply(modifier=mod.name)
# for obj in bpy.data.objects:
#     if 'Cortador_Nicho' in obj.name:
#         obj.hide_set(True)

# --- Iluminación ---
A.agregar_luz('Luz_Salon', tipo='SUN', ubicacion=(10, -10, 10), energia=3)

A.crear_camara('Camara_Salon', ubicacion=(8, 2.25, 1.8), rotacion=(90, 0, 115))