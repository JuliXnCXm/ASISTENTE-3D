import blender_arch as A
import bpy

A.limpiar_escena()

# --- HABITACION ---
habitacion = A.crear_habitacion('SalaEstar', ancho=5, fondo=6, alto=2.8, material_muro='Muro_Pintura_Gris', material_suelo='Parquet')

# --- MOBILIARIO ESTANDAR ---
sofa = A.crear_sofa('SofaPrincipal', ancho=3.0, origen=(1.0, 4.0, 0), material='Tela_Gris')
sofa.rotation_euler[2] = 3.14159 # 180 grados

# --- MUEBLE DE TV Y PANEL DE LISTONES (bpy) ---
# Mueble bajo
bpy.ops.mesh.primitive_cube_add(location=(2.5, 0.4, 0.25))
mueble_tv = bpy.context.active_object
mueble_tv.name = 'MuebleTV'
mueble_tv.scale = (2.0, 0.4, 0.25)
A.asignar_material(mueble_tv, nombre='Madera_Roble')

# Panel de listones vertical
ancho_liston = 0.04
espacio_liston = 0.02
alto_liston = 2.8
num_listones = int(4.0 / (ancho_liston + espacio_liston))

listones = []
for i in range(num_listones):
    x_pos = 0.5 + i * (ancho_liston + espacio_liston)
    bpy.ops.mesh.primitive_cube_add(location=(x_pos, 0.1, alto_liston / 2))
    liston = bpy.context.active_object
    liston.name = f'Liston.{i}'
    liston.scale = (ancho_liston / 2, 0.015, alto_liston / 2)
    listones.append(liston)

# Agrupar listones
for obj in bpy.context.selected_objects:
    obj.select_set(False)

for liston in listones:
    liston.select_set(True)

if listones:
    bpy.context.view_layer.objects.active = listones[0]
    bpy.ops.object.join()
    panel_completo = bpy.context.active_object
    panel_completo.name = 'PanelListones'
    A.asignar_material(panel_completo, nombre='Madera_Roble')

# --- DETALLES ADICIONALES ---
# Alfombra con bpy para control de subdivisiones
bpy.ops.mesh.primitive_plane_add(size=1, location=(2.5, 3.0, 0.01))
alfombra = bpy.context.active_object
alfombra.name = 'Alfombra'
alfombra.scale = (2.0, 3.0, 1.0)
A.asignar_material(alfombra, base_color=(0.2, 0.2, 0.25, 1), nombre='Alfombra_Oscura')
# Añadir grosor con Solidify y suavidad con Bevel
alfombra.modifiers.new(name='Grosor', type='SOLIDIFY').thickness = 0.02
alfombra.modifiers.new(name='Bisel', type='BEVEL').width = 0.01

# Mesa de centro
A.crear_mesa('MesaCentro', ancho=1.2, fondo=0.7, alto=0.4, origen=(2.5, 3.0, 0), material_tablero='MDF_Blanco')

# --- ILUMINACION ---
A.agregar_luz('LuzGeneral', tipo='AREA', ubicacion=(2.5, 3.0, 2.6), energia=250, color=(1, 0.9, 0.8))
luz_area = bpy.data.objects['LuzGeneral'].data
luz_area.shape = 'RECTANGLE'
luz_area.size = 2.0
luz_area.size_y = 3.0