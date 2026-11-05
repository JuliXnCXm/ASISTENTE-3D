import blender_arch as A

A.limpiar_escena()

# Crear la fachada principal
fachada = A.crear_muro(
    nombre="Fachada_Principal",
    largo=8.0,
    alto=6.0,
    grosor=0.3,
    material="Muro_Pintura_Gris"
)

# Crear la losa de balcón en la segunda planta
losa_balcon = A.crear_losa_rectangular(
    nombre="Losa_Balcon",
    ancho=8.0,
    fondo=1.5,
    espesor=0.2,
    origen=(0, -0.3, 3.0),
    material="Hormigon"
)

# Crear la barandilla en la losa del balcón
poste_1 = A.crear_columna("Poste_1", seccion="circ", diametro=0.1, alto=1.0, origen=(-2.5, -0.3, 3.0))
poste_2 = A.crear_columna("Poste_2", seccion="circ", diametro=0.1, alto=1.0, origen=(2.5, -0.3, 3.0))

pasamanos_1 = A.crear_losa_rectangular("Pasamanos_1", ancho=5.0, fondo=0.05, espesor=0.1, origen=(-2.5, -0.35, 4.0), material="Acero_Inox")
pasamanos_2 = A.crear_losa_rectangular("Pasamanos_2", ancho=5.0, fondo=0.05, espesor=0.1, origen=(2.5, -0.35, 4.0), material="Acero_Inox")