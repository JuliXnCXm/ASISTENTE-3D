import blender_arch as A
A.limpiar_escena()
casa = A.crear_casa_n_pisos(nombre='CasaColonial', pisos=2, ancho=15.0, fondo=20.0, alto_piso=3.0, grosor_muro=0.2, grosor_losa=0.2, con_tejado=True, altura_cumbrera=2.0, voladizo=0.5, material_muro='Ladrillo', material_losa='Hormigon', material_tejado='Teja', origen=(0, 0, 0))
A.crear_arbol_simple('ArbolFrontal', radio_copa=3.0, altura_copa=4.0, altura_tronco=2.2, origen=(-4, 6, 0))
A.crear_terreno_plano('Jardin', ancho=25, fondo=25, espesor=0.1, origen=(-12.5, -12.5, 0), material='Cesped')
A.crear_camino('Acceso', ancho=5.0, largo=20, origen=(-12.5, -2, 0), material='Asfalto')