import blender_arch as A
A.limpiar_escena()
huella = 0.28
contrahuella = 0.175
ancho = 1.1
num_peldanos = 14
grosor_peldano = 0.03
con_contrahuellas = True
con_zancas = True
espesor_zanca = 0.15
origen = (0, 0, 0)
material = 'Hormigon'
A.crear_escalera_recta(nombre='EscaleraPrincipal', huella=huella, contrahuella=contrahuella, ancho=ancho, num_peldanos=num_peldanos, grosor_peldano=grosor_peldano, con_contrahuellas=con_contrahuellas, con_zancas=con_zancas, espesor_zanca=espesor_zanca, origen=origen, material=material)
pisos = 2
ancho = 12.0
fondo = 15.0
alto_piso = 2.8
grosor_muro = 0.2
grosor_losa = 0.2
con_columnas = True
seccion_columna = 'rect'
dim_columna = (0.4, 0.4)
modulo_columna_x = 4.0
modulo_columna_y = 5.0
origen = (-6, -7.5, 0)
A.crear_edificio_n_pisos(nombre='EdificioConEscalera', pisos=pisos, ancho=ancho, fondo=fondo, alto_piso=alto_piso, grosor_muro=grosor_muro, grosor_losa=grosor_losa, con_columnas=con_columnas, seccion_columna=seccion_columna, dim_columna=dim_columna, modulo_columna_x=modulo_columna_x, modulo_columna_y=modulo_columna_y, origen=origen)