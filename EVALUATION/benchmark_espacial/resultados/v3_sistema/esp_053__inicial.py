import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='EdificioConBalcones', pisos=3, ancho=20.0, fondo=12.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, material_fachada='Muro_Pintura_Gris', material_losa='Hormigon', material_marco='Marco_Negro')
for i in range(1, 4):
    pos_x = 0
    pos_y = (i - 1) * 3.0 + 0.25 / 2
    A.crear_losa_rectangular(nombre=f'Balcon_{i}', ancho=20.0, fondo=3.0, espesor=0.25, origen=(pos_x, pos_y, i * 3.0), material='Hormigon')
    A.crear_baranda_lineal(nombre=f'Baranda_Balcon_{i}', largo=20.0, altura=1.0, poste_cada=1.5, origen=(pos_x, pos_y, i * 3.0 + 3.0 - 0.25), material='Acero_Inox')