import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='EdificioOficinas', pisos=3, ancho=18.0, fondo=12.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, material_fachada='Muro_Pintura_Gris', material_losa='Hormigon')
ancho_balcon = 3.0
profundidad_balcon = 1.5
alto_baranda = 1.0
pos_y_balcons = [fondo - profundidad_balcon / 2] + [fondo + (i + 1) * (fondo - profundidad_balcon) for i in range(2)]
for i, y_pos in enumerate(pos_y_balcons):
    A.crear_losa_rectangular(nombre=f'Balcon_{i + 1}', ancho=ancho_balcon, fondo=profundidad_balcon, espesor=0.2, origen=(0, y_pos, 0), material='Hormigon')
    A.crear_baranda_lineal(nombre=f'Baranda_Balcon_{i + 1}', largo=ancho_balcon, altura=alto_baranda, origen=(-ancho_balcon / 2, y_pos, 0.2), material='Acero_Inox')