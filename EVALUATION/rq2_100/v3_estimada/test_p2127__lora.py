import blender_arch as A
import bpy

A.limpiar_escena()

# --- ESTRUCTURA Y SUELO ---
A.crear_terreno_plano('Plaza', ancho=20, fondo=20, espesor=0.2, material='Concreto_Piso')
A.crear_columna('Base_Fuente', seccion='circ', diametro=2.5, alto=0.5, origen=(0,0,-0.2), material='Hormigon')
A.crear_columna('Cuerpo_Fuente', seccion='circ', diametro=2.0, alto=1.8, origen=(0,0,0.5), material='Hormigon')
A.crear_columna('Copa_Fuente', seccion='circ', diametro=1.5, alto=1.2, origen=(0,0,2.3), material='Hormigon')

# --- ARBOLADO ---
A.crear_arbol_simple('Arbol_1', radio_copa=2.0, altura_copa=3.5, altura_tronco=1.8, origen=(-6, 6, 0))
A.crear_arbol_simple('Arbol_2', radio_copa=1.8, altura_copa=3.0, altura_tronco=1.5, origen=(6, -5, 0))
A.crear_arbol_simple('Arbol_3', radio_copa=1.5, altura_copa=2.5, altura_tronco=1.2, origen=(-5, -6, 0))

# --- BANCOS DE DISEÑO ---
A.crear_sofa('Banco_1', ancho=2.0, fondo=0.5, alto_asiento=0.45, origen=(-4, 4, 0), material='Madera_Roble')
A.crear_sofa('Banco_2', ancho=2.0, fondo=0.5, alto_asiento=0.45, origen=(4, -3, 0), material='Madera_Roble')
A.crear_sofa('Banco_3', ancho=2.0, fondo=0.5, alto_asiento=0.45, origen=(-3, -4, 0), material='Madera_Roble')
A.crear_sofa('Banco_4', ancho=2.0, fondo=0.5, alto_asiento=0.45, origen=(3, 3, 0), material='Madera_Roble')