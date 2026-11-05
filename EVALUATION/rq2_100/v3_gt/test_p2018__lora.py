import blender_arch as A
import bpy

A.limpiar_escena()

# --- Estructura y Materiales ---
muro = A.crear_muro('MuroEscalera', largo=2.5, alto=2.8, grosor=0.2, origen=(0,0,-0.1), material='Muro_Pintura_Gris')
piso = A.crear_losa_rectangular('PisoBase', ancho=2.5, fondo=0.6, espesor=0.1, origen=(0,0,0), material='Concreto_Piso')

# --- Peldanos Flotantes con blender_arch ---
num_peldanos = 12
ancho_peldano = 0.2
grosor_peldano = 0.05
for i in range(num_peldanos):
    pos_x = -0.5 + i * (2.5 / num_peldanos)
    pos_y = 0.3
    pos_z = 0.1 + i * 0.15
    
    # Crear el peldano
    bpy.ops.mesh.primitive_cube_add(location=(pos_x, pos_y, pos_z))
    peldano = bpy.context.active_object
    peldano.name = f"Peldano_{i+1}"
    peldano.dimensions = (ancho_peldano, grosor_peldano, 0.2)
    A.asignar_material(peldano, nombre="Madera_Roble", base_color=(0.9, 0.7, 0.5, 1))

# --- Baranda de Vidrio con bpy ---
alto_baranda = 1.0
ancho_baranda = 2.5
grosor_baranda = 0.05
for i in range(num_peldanos):
    pos_x = -0.5 + i * (2.5 / num_peldanos)
    pos_y = 0.3 + 0.15
    pos_z = 0.1 + i * 0.15 + alto_baranda/2
    
    # Crear panel de vidrio
    bpy.ops.mesh.primitive_cube_add(location=(pos_x, pos_y, pos_z))
    panel_vidrio = bpy.context.active_object
    panel_vidrio.name = f"PanelVidrio_{i+1}"
    panel_vidrio.dimensions = (ancho_baranda, grosor_baranda, alto_baranda)
    A.asignar_material(panel_vidrio, nombre="Vidrio_Templado", base_color=(0.9, 0.9, 0.9, 1))

# --- Pasamanos Metálico con bpy ---
alto_pasamanos = 0.9
ancho_pasamanos = 0.1
grosor_pasamanos = 0.02
for i in range(num_peldanos):
    pos_x = -0.5 + i * (2.5 / num_peldanos)
    pos_y = 0.3 + 0.15 + alto_baranda/2
    pos_z = 0.1 + i * 0.15 + alto_baranda + alto_pasamanos/2
    
    # Crear percha del pasamanos
    bpy.ops.mesh.primitive_cube_add(location=(pos_x, pos_y, pos_z))
    percha = bpy.context.active_object
    percha.name = f"Percha_{i+1}"
    percha.dimensions = (grosor_pasamanos, ancho_pasamanos, alto_pasamanos)
    A.asignar_material(percha, nombre="Acero_Inox", base_color=(0.8, 0.8, 0.8, 1))