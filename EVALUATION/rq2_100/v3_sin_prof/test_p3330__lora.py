import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA DE LA TERRAZA ---
A.crear_losa_rectangular('Losa_Terraza', ancho=8, fondo=8, espesor=0.2, origen=(0,0,-0.2), material='Concreto_Piso')
A.crear_pared('Muro_Fondo', largo=8, alto=2.5, grosor=0.2, origen=(0,0,0), material='Hormigon')
A.crear_pared('Muro_Izq', largo=8, alto=2.5, grosor=0.2, origen=(0,0,0), rotacion_z=-90, material='Hormigon')
A.crear_pared('Muro_Der', largo=8, alto=2.5, grosor=0.2, origen=(8,0,0), rotacion_z=90, material='Hormigon')

# --- PÉRGOLA DE DESCANSO ---
A.crear_barra('Pergola_Sureste', largo=4, alto=2.5, origen=(4,4,0), material='Acero_Inox')
A.crear_barra('Pergola_Sureste', largo=4, alto=2.5, origen=(4,4,0), rotacion_z=90, material='Acero_Inox')
A.crear_barra('Pergola_Noreste', largo=4, alto=2.5, origen=(4,4,0), material='Acero_Inox')
A.crear_barra('Pergola_Noreste', largo=4, alto=2.5, origen=(4,4,0), rotacion_z=90, material='Acero_Inox')

# --- JARDINERÍA PERIMETRAL ---
for i in range(4):
    A.crear_hormigon('Jardinera_{}.{}'.format(i+1,1), ancho=2, fondo=0.5, alto=0.5, origen=(i*2+0.5,0.5,0), material='Hormigon')
    A.crear_hormigon('Jardinera_{}.{}'.format(i+1,2), ancho=0.5, fondo=2, alto=0.5, origen=(0,i*2+0.5,0), material='Hormigon')
    A.crear_planta('Planta_{}.{}'.format(i+1,1), radio=0.2, altura=0.3, origen=(i*2+0.5,0.5,0.5), material='Hormigon')
    A.crear_planta('Planta_{}.{}'.format(i+1,2), radio=0.2, altura=0.3, origen=(0,i*2+0.5,0.5), material='Hormigon')

# --- SUELO DE DECK ---
A.crear_piso('Deck', ancho=6, fondo=6, espesor=0.15, origen=(1,1,0.2), material='Madera_Deck')