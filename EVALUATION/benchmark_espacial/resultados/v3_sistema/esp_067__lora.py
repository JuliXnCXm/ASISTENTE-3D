import blender_arch as A

A.limpiar_escena()

# Edificio base
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Corporativo",
    pisos=6,
    ancho=18.0,
    fondo=10.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Ático sobre la cubierta
ancho_atico = 3.0
fondo_atico = 4.0
alto_atico = 2.5

# Calcular posición del ático
altura_cubierta = 6 * 3.0
pos_x_atico = (18.0 - ancho_atico) / 2
pos_y_atico = (10.0 - fondo_atico) / 2
pos_z_atico = altura_cubierta + alto_atico / 2

A.crear_habitacion(
    nombre="Atico",
    ancho=ancho_atico,
    fondo=fondo_atico,
    alto=alto_atico,
    origen=(pos_x_atico, pos_y_atico, pos_z_atico),
    material_muro="Muro_Pintura_Blanco",
    material_suelo="Porcelanato"
)