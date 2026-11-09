import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='Edificio_Casa', pisos=3, ancho=16.0, fondo=12.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, con_columnas=False, origen=(0, 0, 0), material_muro='Muro_Pintura_Gris', material_losa='Hormigon')
for i in range(1, 4):
    x_pos = -15.5 + 0.25
    y_pos = i * 3.0 - 1.5
    A.crear_losa_rectangular(f'Balcon_{i}', ancho=3.0, fondo=1.5, espesor=0.2, origen=(x_pos, y_pos, 0), material='Hormigon')
    A.crear_baranda_lineal(f'Baranda_{i}', largo=3.0, origen=(x_pos, y_pos, 0.2), material='Acero_Inox')