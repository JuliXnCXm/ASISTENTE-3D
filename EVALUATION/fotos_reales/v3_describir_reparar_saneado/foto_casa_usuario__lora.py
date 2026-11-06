import blender_arch as A
A.limpiar_escena()
casa = A.crear_casa_n_pisos(nombre='CasaFamiliar', pisos=2, ancho=15.0, fondo=20.0, alto_piso=2.8, con_tejado=True, altura_cumbrera=2.0, voladizo=0.5, origen=(0, 0, 0), material_muro='Estuco', material_losa='Hormigon', material_tejado='Teja')
A.crear_coche('Coche1', ancho=2.0, fondo=0.9, alto_casco=1.7, origen=(-4, -3, 0), material='Acero')
A.crear_coche('Coche2', ancho=2.0, fondo=0.9, alto_casco=1.7, origen=(4, -3, 0), material='Acero')
A.agregar_luz('LuzSol', tipo='SUN', ubicacion=(5, -10, 10), energia=3)
A.crear_camara('CamaraFrontal', ubicacion=(0, -15, 5), rotacion=(80, 0, 0))