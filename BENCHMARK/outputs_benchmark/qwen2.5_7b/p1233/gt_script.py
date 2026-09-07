import blender_arch as A

A.limpiar_escena()
# Terreno con superficie en Z=0
A.crear_terreno_plano('Parcela', ancho=20, fondo=20, espesor=0.2, origen=(0,0,-0.1), material='Cesped')

# Casa centrada en el origen (0,0,0)
A.crear_casa_n_pisos('Casa_Familiar', pisos=2, ancho=10.0, fondo=8.0, alto_piso=2.8, con_tejado=True, altura_cumbrera=2.0, voladizo=0.5, origen=(-5, -4, 0), material_muro='Estuco', material_losa='Hormigon', material_tejado='Teja')

# Arboles en el terreno
A.crear_arbol_simple('Arbol_1', radio_copa=2.0, altura_copa=3.5, altura_tronco=2.0, origen=(-8, 7, 0))
A.crear_arbol_simple('Arbol_2', radio_copa=1.5, altura_copa=3.0, altura_tronco=1.5, origen=(8, -6, 0))