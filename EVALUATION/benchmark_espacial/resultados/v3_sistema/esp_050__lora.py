import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='Edificio_Casa', pisos=4, ancho=14.0, fondo=8.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, con_columnas=False, origen=(0, 0, 0), material_fachada='Muro_Pintura_Gris', material_losa='Hormigon', material_marco='Marco_Negro')
for i in range(1, 5):
    z_piso = (i - 1) * 3.0
    x_balcon = 7.0 - 1.5 / 2
    y_balcon = -8.0 + 1.5 / 2
    A.crear_losa_rectangular(nombre=f'Balcon_{i}', ancho=3.0, fondo=1.5, espesor=0.2, origen=(x_balcon, y_balcon, z_piso), material='Hormigon')
    A.crear_baranda_lineal(nombre=f'Baranda_Balcon_{i}', largo=3.0, altura=0.9, poste_cada=0.6, origen=(x_balcon, y_balcon, z_piso + 0.2), material='Acero_Inox')