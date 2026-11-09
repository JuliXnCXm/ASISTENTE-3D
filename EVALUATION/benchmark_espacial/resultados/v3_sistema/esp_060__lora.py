import blender_arch as A
A.limpiar_escena()
edificio = A.crear_edificio_n_pisos(nombre='Edificio_Corporativo', pisos=5, ancho=18.0, fondo=12.0, alto_piso=3.0, grosor_muro=0.25, con_techo_plano=True, material_muro='Muro_Pintura_Gris', material_losa='Hormigon')
origen_volumen = (18.0 / 2 - 2.5, 12.0 / 2 - 2.0, 3.0 * 5)
volumen_solar = A.extruir_perfil('Volumen_Solar_Perfil', puntos_2d=[[0, 0], [5.0, 0], [5.0, 4.0], [0, 4.0], [0, 0]], altura=2.5).location = origen_volumen
A.asignar_material(volumen_solar, 'Marco_Aluminio')