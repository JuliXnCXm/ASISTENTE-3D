import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='EdificioConBalcones', pisos=4, ancho=18.0, fondo=12.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, material_fachada='Muro_Pintura_Gris', material_losa='Hormigon', material_marco='Marco_Negro', material_vidrio='Vidrio')
ancho_balcon = 3.0
fondo_balcon = 1.5
alto_piso = 3.0
num_pisos = 4
for i in range(1, num_pisos + 1):
    z_pos = (i - 1) * alto_piso
    A.crear_losa_rectangular(nombre=f'Balcon_{i}', ancho=ancho_balcon, fondo=fondo_balcon, espesor=0.2, origen=(0, -fondo_balcon / 2 + fondo_balcon / 2, z_pos), material='Hormigon')
    A.crear_baranda_lineal(nombre=f'Baranda_Balcon_{i}', largo=ancho_balcon, altura=0.9, poste_cada=1.0, origen=(-ancho_balcon / 2, -fondo_balcon / 2, z_pos + fondo_balcon), material='Acero_Inox')