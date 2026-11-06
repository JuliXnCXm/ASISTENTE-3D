import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='Rascacielos_Corporativo', pisos=45, ancho=100.0, fondo=100.0, alto_piso=3.6, grosor_muro=0.25, grosor_losa=0.3, con_columnas=True, seccion_columna='rect', dim_columna=0.4, modulo_columna_x=10.0, modulo_columna_y=10.0, ventanas_fachada=True, ventana_ancho=2.0, ventana_alto=2.2, ventana_alfeizar=0.2, ventana_separacion=3.0, material_fachada='Muro_Pintura_Gris', material_losa='Hormigon', material_vidrio='Vidrio_Templado', material_marco='Marco_Aluminio', material_columna='Hormigon_Visto', origen=(0, 0, 0))
for i in range(45):
    for j in [-1, 0, 1]:
        for k in [-1, 0, 1]:
            if j == 0 and k == 0:
                continue
            x = -5 + i * 10 + 5 * j
            z = 2.5 + i * 3.6 + 1.5 * k
            A.crear_baranda_lineal(f'Baranda_{i}_{j}_{k}', largo=10, origen=(x, -5, z), material='Acero_Inox')
for i in range(10):
    A.crear_escalera_recta(nombre=f'EscaleraExterior_{i}', huella=0.28, contrahuella=0.175, ancho=1.5, num_peldanos=45, origen=(-8, -8, 0), material='Acero_Inox')