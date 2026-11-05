import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA Y MATERIALES ---
muro = A.crear_muro('MuroEscalera', largo=3.5, alto=2.8, grosor=0.2, origen=(0,0,-0.1), material='Muro_Pintura_Gris')
piso = A.crear_piso('PisoBase', ancho=3.5, fondo=0.6, espesor=0.05, origen=(0,0,0), material='Concreto_Piso')

# --- PELDAÑOS FLOTANTES (bpy) ---
num_peldanos = 12
ancho_peldano = 0.25
alto_peldano = 0.18
grosor_panel = 0.02

for i in range(num_peldanos):
    pos_x = (i * ancho_peldano) + (ancho_peldano / 2)
    pos_z = (i * alto_peldano) + (alto_peldano / 2)
    
    bpy.ops.mesh.primitive_cube_add(location=(pos_x, 0, pos_z))
    peldano = bpy.context.active_object
    peldano.name = f"Peldano_{i+1}"
    peldano.dimensions = (ancho_peldano, grosor_panel, alto_peldano)
    A.asignar_material(peldano, nombre="Madera_Roble", base_color=(0.4, 0.2, 0.1, 1))

# --- BARANDA DE VIDRIO (bpy) ---
panel_vidrio = A.crear_losa_rectangular('PanelBaranda', ancho=3.5, fondo=0.05, espesor=0.02, origen=(0, -0.025, 1.2), material='Vidrio_Templado')
panel_baranda = A.crear_losa_rectangular('PanelBarandaPoste', ancho=0.05, fondo=0.05, espesor=0.02, origen=(-1.7, 0, 1.2), material='Acero_Inox')

# --- PASAMANOS METÁLICO (bpy) ---
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1.2))
pasamano = bpy.context.active_object
pasamano.name = "Pasamano"
pasamano.dimensions = (3.5, 0.02, 0.05)
A.asignar_material(pasamano, nombre="Acero_Inox")

# --- ILUMINACIÓN Y CÁMARA ---
A.agregar_luz('LuzEscalera', tipo='AREA', ubicacion=(0, 0, 3.5), energia=150)
A.crear_camara('CamaraEscalera', ubicacion=(0, -4, 1.5), rotacion=(80, 0, 0))