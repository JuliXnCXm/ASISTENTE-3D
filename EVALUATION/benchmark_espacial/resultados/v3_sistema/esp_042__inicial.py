import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='Edificio_Casa', pisos=4, ancho=18.0, fondo=12.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')
ancho_balcon = 3.0
fondo_balcon = 1.5
alto_baranda = 1.0
for i in range(1, 5):
    pos_x = 9.0 - ancho_balcon / 2
    pos_y = 6.0 + fondo_balcon / 2 + 0.1
    A.crear_losa_rectangular(nombre=f'Balcon_{i}', ancho=ancho_balcon, fondo=fondo_balcon, espesor=0.2, origen=(pos_x, pos_y, i * 3.0), material='Hormigon')
    A.crear_baranda_lineal(nombre=f'Baranda_Balcon_{i}', largo=ancho_balcon, altura=alto_baranda, origen=(pos_x, pos_y, i * 3.0 + 0.2), material='Acero_Inox')