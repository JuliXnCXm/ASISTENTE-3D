import blender_arch as A
A.limpiar_escena()
ancho, fondo, alto = 6.0, 4.0, 3.0
grosor_muro, grosor_losa = 0.2, 0.2

# Estructura de la habitación
A.crear_piso("Suelo_Comedor", ancho, fondo, espesor=grosor_losa, material="Porcelanato")
A.crear_techo_plano("Techo_Comedor", ancho, fondo, espesor=grosor_losa, origen=(0, 0, alto), material="Yeso")
muro_frente = A.crear_muro("Muro_Frente", ancho, alto, grosor_muro, origen=(-ancho/2, fondo/2 - grosor_muro/2, grosor_losa), material="Estuco")
A.crear_muro("Muro_Trasero", ancho, alto, grosor_muro, origen=(-ancho/2, -fondo/2 + grosor_muro/2, grosor_losa), material="Estuco")
A.crear_muro("Muro_Izquierda", fondo, alto, grosor_muro, origen=(-ancho/2 + grosor_muro/2, -fondo/2, grosor_losa), rotacion_z=90, material="Estuco")
A.crear_muro("Muro_Derecha", fondo, alto, grosor_muro, origen=(ancho/2 - grosor_muro/2, -fondo/2, grosor_losa), rotacion_z=90, material="Estuco")

# Ventana en el muro frontal
ventana_ancho, ventana_alto = 2.5, 1.5
ventana_z = grosor_losa + 0.9
centro_vano = (0, fondo/2 - grosor_muro/2, ventana_z + ventana_alto/2)
A.crear_ventana("Ventana_Comedor", ventana_ancho, ventana_alto, prof_marco=grosor_muro, origen=(centro_vano[0] - ventana_ancho/2, centro_vano[1] - grosor_muro/2, ventana_z), material_marco="Marco_Aluminio", material_vidrio="Vidrio")
A.abrir_vanos_batch_rectangulares(muro_frente, [centro_vano], ventana_ancho, ventana_alto)

# Mobiliario
mesa_ancho, mesa_fondo = 2.0, 0.9
A.crear_mesa("Mesa_Comedor", ancho=mesa_ancho, fondo=mesa_fondo, alto=0.76, origen=(0, 0, grosor_losa), material_tablero="Madera_Nogal")
espacio_silla_x = 0.8
for i in range(3):
    x_pos = -espacio_silla_x + i * espacio_silla_x
    A.crear_silla(f"Silla_{i+1}", origen=(x_pos, mesa_fondo/2 + 0.35, grosor_losa), material="Cuero")
    silla_opuesta = A.crear_silla(f"Silla_{i+4}", origen=(x_pos, -mesa_fondo/2 - 0.35, grosor_losa), material="Cuero")

# Iluminación
A.agregar_luz("Luz_Comedor", tipo="AREA", ubicacion=(0, 0, alto - 0.1), energia=600, color=(1.0, 0.9, 0.8))