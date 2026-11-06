import blender_arch as A
A.limpiar_escena()
casa = A.crear_casa_n_pisos(nombre='CasaColonial', pisos=2, ancho=20.0, fondo=15.0, alto_piso=3.0, grosor_muro=0.25, grosor_losa=0.2, con_tejado=True, altura_cumbrera=2.0, voladizo=0.5, material_muro='Ladrillo', material_losa='Hormigon', material_tejado='Teja_Negra', origen=(0, 0, 0))
A.crear_losa_rectangular('PavimentoAcceso', ancho=12, fondo=12, espesor=0.15, origen=(-10, -10, 0), material='Asfalto')
A.crear_terreno_plano('Jardin', ancho=30, fondo=25, espesor=0.3, origen=(-15, -15, -0.15), material='Cesped')
A.crear_arbol_simple('Arbol1', origen=(-8, 7, 0))
A.crear_arbol_simple('Arbol2', origen=(8, 7, 0))