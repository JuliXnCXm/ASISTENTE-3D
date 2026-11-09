import blender_arch as A
A.limpiar_escena()
ancho = 12.0
fondo = 10.0
alto_piso = 3.0
grosor_muro = 0.25
altura_cumbrera = 2.0
angulo_cumbrera = 10.0
vol_casa = A.crear_habitacion(nombre='Casa', ancho=ancho, fondo=fondo, alto=alto_piso + altura_cumbrera, grosor_muro=grosor_muro, material_muro='Muro_Pintura_Gris', material_suelo='Concreto_Piso', material_techo='Teja')
vol_techo = A.crear_techo_plano(nombre='Techo', ancho=ancho, fondo=fondo, espesor=altura_cumbrera, origen=(0, 0, alto_piso), material='Teja')
voladizo_x = ancho / 2 - grosor_muro * 2
voladizo_y = grosor_muro
voladizo_z = altura_cumbrera
corte_techo = A.crear_caja(nombre='Corte_Techo', ancho=voladizo_x, fondo=voladizo_y, alto=voladizo_z, origen=(-voladizo_x / 2, -voladizo_y / 2, voladizo_z / 2))
mod_bool = vol_techo.modifiers.new(name='BooleanVoladizo', type='BOOLEAN')
mod_bool.object = corte_techo
mod_bool.operation = 'DIFFERENCE'
A.asignar_material(vol_techo, 'Teja', base_color=(0.4, 0.6, 0.8, 1))
A.agregar_luz('Luz_Solar', tipo='SUN', ubicacion=(-10, -10, 15), energia=5)
A.crear_camara('Camara_Frontal', ubicacion=(0, -15, 5), rotacion=(90, 0, 0))