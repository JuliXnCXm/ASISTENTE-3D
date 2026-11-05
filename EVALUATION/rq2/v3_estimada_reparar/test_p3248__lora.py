import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='EdificioOficinas', pisos=4, ancho=15.0, fondo=20.0, alto_piso=3.2, grosor_muro=0.3, con_techo_plano=True, con_columnas=False, material_fachada='Muro_Pintura_Gris', material_losa='Hormigon', material_tejado='Teja')
for i in range(4):
    x_pos = -15.0 / 2 + 0.9 + i * 3.0
    A.crear_losa_rectangular(f'Balcon_{i + 1}', ancho=3.0, fondo=0.9, espesor=0.2, origen=(x_pos, -20.0 / 2, 2.6), material='Concreto_Piso')
for i in range(4):
    x_pos = -15.0 / 2 + 0.9 + i * 3.0
    A.crear_losa_rectangular(f'Jardinera_{i + 1}', ancho=0.5, fondo=0.5, espesor=0.4, origen=(x_pos, -20.0 / 2, 4.0), material='Hormigon')
A.agregar_luz('LuzPrincipal', tipo='SUN', ubicacion=(-10, -10, 15), energia=3)
A.crear_camara('CamaraFrontal', ubicacion=(0, -25, 5), rotacion=(80, 0, 0))