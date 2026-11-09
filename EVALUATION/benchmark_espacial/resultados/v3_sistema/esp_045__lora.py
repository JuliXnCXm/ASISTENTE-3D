import blender_arch as A

A.limpiar_escena()

# Crear el edificio base
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioConBalcones",
    pisos=4,
    ancho=12.0,
    fondo=12.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Definir parámetros del balcón
ancho_balcon = 3.0
fondo_balcon = 1.5
alto_baranda = 1.0

# Crear balcón en el primer piso
A.crear_losa_rectangular(
    nombre="Balcon_Piso1",
    ancho=ancho_balcon,
    fondo=fondo_balcon,
    espesor=0.2,
    origen=(0, -fondo_balcon/2, 3.0),
    material="Hormigon"
)
A.crear_baranda_lineal(
    nombre="Baranda_Piso1",
    largo=ancho_balcon,
    altura=alto_baranda,
    origen=(-ancho_balcon/2, -fondo_balcon/2, 3.2),
    material="Acero_Inox"
)

# Crear balcón en el segundo piso
A.crear_losa_rectangular(
    nombre="Balcon_Piso2",
    ancho=ancho_balcon,
    fondo=fondo_balcon,
    espesor=0.2,
    origen=(0, -fondo_balcon/2, 6.0),
    material="Hormigon"
)
A.crear_baranda_lineal(
    nombre="Baranda_Piso2",
    largo=ancho_balcon,
    altura=alto_baranda,
    origen=(-ancho_balcon/2, -fondo_balcon/2, 6.2),
    material="Acero_Inox"
)

# Crear balcón en el tercer piso
A.crear_losa_rectangular(
    nombre="Balcon_Piso3",
    ancho=ancho_balcon,
    fondo=fondo_balcon,
    espesor=0.2,
    origen=(0, -fondo_balcon/2, 9.0),
    material="Hormigon"
)
A.crear_baranda_lineal(
    nombre="Baranda_Piso3",
    largo=ancho_balcon,
    altura=alto_baranda,
    origen=(-ancho_balcon/2, -fondo_balcon/2, 9.2),
    material="Acero_Inox"
)

# Crear balcón en el cuarto piso
A.crear_losa_rectangular(
    nombre="Balcon_Piso4",
    ancho=ancho_balcon,
    fondo=fondo_balcon,
    espesor=0.2,
    origen=(0, -fondo_balcon/2, 12.0),
    material="Hormigon"
)
A.crear_baranda_lineal(
    nombre="Baranda_Piso4",
    largo=ancho_balcon,
    altura=alto_baranda,
    origen=(-ancho_balcon/2, -fondo_balcon/2, 12.2),
    material="Acero_Inox"
)