import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioOficinas",
    pisos=4,
    ancho=12.0,
    fondo=14.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Ático sobre la cubierta
alto_edificio = 4 * 3.0
ancho_atico = 5.0
fondo_atico = 3.0
grosor_atico = 0.3

# Calcular posición del ático
pos_x_atico = (12.0 - ancho_atico) / 2
pos_y_atico = (14.0 - fondo_atico) / 2
pos_z_atico = alto_edificio + grosor_atico / 2

A.crear_losa_rectangular(
    nombre="LosaAtico",
    ancho=ancho_atico,
    fondo=fondo_atico,
    espesor=grosor_atico,
    origen=(pos_x_atico, pos_y_atico, pos_z_atico),
    material="Hormigon"
)