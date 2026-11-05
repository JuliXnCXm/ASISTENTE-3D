import blender_arch as A
import bpy

A.limpiar_escena()

# --- Estructura y suelo ---
A.crear_losa_rectangular('Losa_Terraza', ancho=10, fondo=8, espesor=0.2, origen=(0,0,-0.2), material='Concreto_Piso')
A.crear_piso('Deck_Madera', ancho=10, fondo=8, espesor=0.05, origen=(0,0,0.25), material='Madera_Roble')

# --- Pérgola ---
A.crear_barra('Pergola_Principal_1', largo=10, alto=2.5, origen=(-5, -4, 0.25), material='Acero_Inox')
A.crear_barra('Pergola_Principal_2', largo=10, alto=2.5, origen=(5, -4, 0.25), material='Acero_Inox')
A.crear_barra('Pergola_Secundaria_1', largo=4, alto=2.5, origen=(-5, 4, 0.25), material='Acero_Inox')
A.crear_barra('Pergola_Secundaria_2', largo=4, alto=2.5, origen=(5, 4, 0.25), material='Acero_Inox')

# --- Jardineras ---
for i in [-4, 4]:
    for j in [-4, 4]:
        A.extruir_con_huecos('Jardinera_{}'.format(i,j), 
            contorno=[(-1.5, -1.5), (1.5, -1.5), (1.5, 1.5), (-1.5, 1.5)], 
            agujeros=[[(0,0)]], 
            altura=0.3, 
            material='Hormigon')
        jardinera = bpy.data.objects['Jardinera_{}{}'.format(i,j)]
        jardinera.location.x = i * 2.5 + 0.75
        jardinera.location.y = j * 2.5 + 0.75
        jardinera.rotation_euler[2] = 1.5708 # 90 grados

# --- Vegetación ---
for i in [-4, 4]:
    for j in [-4, 4]:
        if i == 0 and j == 0:
            continue
        A.crear_arbol_simple('Arbol_{}'.format(i,j), radio_copa=1.0, altura_copa=2.0, altura_tronco=1.5, origen=(i*2.5+0.75, j*2.5+0.75, 0.25))