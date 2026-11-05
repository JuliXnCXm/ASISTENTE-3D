import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='IceHouse', pisos=4, ancho=20.0, fondo=15.0, alto_piso=3.2, grosor_muro=0.25, grosor_losa=0.3, material_muro='Ladrillo', material_losa='Hormigon', origen=(0, 0, 0))
A.crear_losa_rectangular('Pavimento_Calle', ancho=50, fondo=30, espesor=0.15, origen=(-25, -15, 0), material='Concreto_Piso')
A.crear_sofa('Sofa_Exterior_1', ancho=2.5, fondo=0.9, origen=(-10, -2, 0), material='Tela_Gris')
A.crear_sofa('Sofa_Exterior_2', ancho=2.5, fondo=0.9, origen=(10, -2, 0), material='Tela_Gris')
A.agregar_luz('Luz_Solar', tipo='SUN', ubicacion=(10, -10, 20), energia=2.5)
A.crear_camara('Camara_Frontal', ubicacion=(-15, -20, 10), rotacion=(70, 0, 0))