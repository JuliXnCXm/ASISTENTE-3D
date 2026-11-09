import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='EdificioOficinas', pisos=4, ancho=12.0, fondo=14.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')
ancho_balcon = 3.0
profundidad_balcon = 1.5
alto_baranda = 1.0
pos_x_balcon = (ancho_balcon - 0.2) / 2
pos_y_balcon = (profundidad_balcon - 0.2) / 2
altura_piso = 3.0
for i in range(1, 5):
    pos_x_piso = i * ancho_balcon + pos_x_balcon
    A.crear_losa_rectangular(nombre=f'Balcon_{i}', ancho=ancho_balcon, fondo=profundidad_balcon, espesor=0.2, origen=(pos_x_piso, pos_y_balcon, altura_piso), material='Hormigon')
    A.crear_baranda_lineal(nombre=f'Baranda_{i}', largo=ancho_balcon, altura=alto_baranda, origen=(pos_x_piso, pos_y_balcon, altura_piso + profundidad_balcon / 2), material='Acero_Inox')