import blender_arch as A

A.limpiar_escena()

# --- Parámetros generales ---
ancho_total = 10.0
fondo_total = 8.0
alto_piso = 2.8
grosor_muro = 0.2
grosor_losa = 0.2
material_muro = 'Muro_Pintura'
material_suelo = 'Suelo_Madera'
material_techo = 'Losacero'

# --- Crear la casa ---
casa = A.crear_casa_n_pisos(
    nombre="Apartamento",
    pisos=2,
    ancho=ancho_total,
    fondo=fondo_total,
    alto_piso=alto_piso,
    grosor_muro=grosor_muro,
    grosor_losa=grosor_losa,
    con_tejado=True,
    altura_cumbrera=1.5,
    voladizo=0.4,
    origen=(0, 0, 0),
    material_muro=material_muro,
    material_losa=material_suelo,
    material_tejado="Teja"
)

# --- Crear el piso superior ---
piso_superior = A.crear_piso(nombre="PisoSuperior", ancho=ancho_total, fondo=fondo_total, espesor=0.05, origen=(0, 0, alto_piso), material=material_suelo)

# --- Crear habitaciones y áreas comunes ---
# Sala-Comedor
hab_sala = A.crear_habitacion(nombre="SalaComedor", ancho=5.0, fondo=4.0, alto=alto_piso, grosor_muro=grosor_muro, grosor_losa=grosor_losa, origen=(0, 0, 0), material_muro=material_muro, material_suelo=material_suelo, material_techo=material_techo)
# Cocina
hab_cocina = A.crear_habitacion(nombre="Cocina", ancho=3.0, fondo=2.5, alto=alto_piso, grosor_muro=grosor_muro, grosor_losa=grosor_losa, origen=(ancho_total - 3.0, 0, 0), material_muro=material_muro, material_suelo=material_suelo, material_techo=material_techo)
# Barra de cocina
barra_cocina = A.crear_piso(nombre="BarraCocina", ancho=1.2, fondo=0.6, espesor=0.05, origen=(ancho_total - 1.8, 2.45, 0), material=material_suelo)
# Pasillo
pasillo = A.crear_habitacion(nombre="Pasillo", ancho=1.5, fondo=2.5, alto=alto_piso, grosor_muro=grosor_muro, grosor_losa=grosor_losa, origen=(ancho_total - 3.0, 2.5, 0), material_muro=material_muro, material_suelo=material_suelo, material_techo=material_techo)
# Baño
hab_bano = A.crear_habitacion(nombre="Bano", ancho=2.5, fondo=2.0, alto=alto_piso, grosor_muro=grosor_muro, grosor_losa=grosor_losa, origen=(ancho_total - 3.0, 5.0, 0), material_muro=material_muro, material_suelo=material_suelo, material_techo=material_techo)
# Dormitorio
hab_dormitorio = A.crear_habitacion(nombre="Dormitorio", ancho=4.0, fondo=4.0, alto=alto_piso, grosor_muro=grosor_muro, grosor_losa=grosor_losa, origen=(ancho_total - 4.0, 7.0, 0), material_muro=material_muro, material_suelo=material_suelo, material_techo=material_techo)

# --- Mobiliario ---
# Armario en el pasillo
armario_pasillo = A.crear_armario(nombre="ArmarioPasillo", ancho=1.8, alto=2.4, fondo=0.6, num_puertas=2, origen=(ancho_total - 1.8, 2.5 - 0.6/2 - 0.1, 0), material_cuerpo="Madera", material_puerta="Madera_Lacada")

# --- Ventanas ---
# Sala-Comedor
A.abrir_vanos_batch_rectangulares(hab_sala, centros_world=[(ancho_total/2, 0.2, alto_piso/2)], ancho=2.0, alto=1.2)
# Cocina
A.abrir_vanos_batch_rectangulares(hab_cocina, centros_world=[(ancho_total - 3.0 - 0.2, 2.5 - 0.2, alto_piso/2)], ancho=1.2, alto=1.1)
# Pasillo
A.abrir_vanos_batch_rectangulares(pasillo, centros_world=[(ancho_total - 3.0 - 0.2, 2.5 - 0.2, alto_piso/2)], ancho=1.2, alto=1.1)
# Dormitorio
A.abrir_vanos_batch_rectangulares(hab_dormitorio, centros_world=[(ancho_total - 4.0 - 0.2, 7.0 - 0.2, alto_piso/2)], ancho=1.2, alto=1.1)

# --- Iluminación y cámara ---
A.agregar_luz(nombre="LuzPrincipal", tipo="AREA", ubicacion=(ancho_total/2, fondo_total/2, alto_piso+2), energia=200)
A.crear_camara(nombre="Camara", ubicacion=(-5, -5, 5), rotacion=(70, 0, -45), activa=True)