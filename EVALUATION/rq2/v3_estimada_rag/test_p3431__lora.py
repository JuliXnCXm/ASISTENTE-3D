import blender_arch as A

A.limpiar_escena()

# --- Parámetros de la cocina ---
ancho_total = 5.0
fondo_total = 4.0
alto_piso = 2.8
grosor_muro = 0.2
grosor_losa = 0.2
ancho_isla = 2.0
fondo_isla = 1.0

# --- Materiales ---
mat_muro = 'Muro_Pintura'
mat_piso = 'Suelo_Madera'
mat_encimera = 'Cuarzo_Blanco'
mat_metal = 'Acero_Inox'
mat_madera = 'Madera_Roble'

# --- Crear la base de la cocina ---
hab = A.crear_habitacion(
    nombre="Cocina",
    ancho=ancho_total,
    fondo=fondo_total,
    alto=alto_piso,
    grosor_muro=grosor_muro,
    grosor_losa=grosor_losa,
    origen=(0, 0, 0),
    material_muro=mat_muro,
    material_suelo=mat_piso,
    material_techo="Yeso"
)

# --- Módulos bajos ---
num_muebles_bajos = 6
ancho_mueble = 0.6
fondo_mueble = 0.6
alto_mueble = 0.85
for i in range(num_muebles_bajos):
    x_pos = (ancho_total / 2) - (ancho_mueble * (num_muebles_bajos / 2)) + (i * ancho_mueble)
    y_pos = fondo_total - (fondo_mueble * 1.5)
    A.crear_estanteria(
        nombre=f"MuebleBajo_{i}",
        ancho=ancho_mueble,
        alto=alto_mueble,
        fondo=fondo_mueble,
        num_estantes=1,
        grosor_tablero=0.025,
        origen=(x_pos, y_pos, 0),
        material=mat_madera
    )

# --- Encimera ---
A.crear_piso(
    nombre="Encimera",
    ancho=ancho_total,
    fondo=fondo_total,
    espesor=0.04,
    origen=(0, 0, alto_piso),
    material=mat_encimera
)

# --- Isla central ---
ancho_isla = 2.0
fondo_isla = 1.0
alto_isla = alto_piso + 0.9
origen_isla = (ancho_total / 2, fondo_total - fondo_isla - 0.1, 0)
A.crear_piso(
    nombre="TableroIsla",
    ancho=ancho_isla,
    fondo=fondo_isla,
    espesor=0.04,
    origen=origen_isla,
    material=mat_madera
)
A.crear_piso(
    nombre="BaseIsla",
    ancho=ancho_isla,
    fondo=fondo_isla,
    espesor=alto_isla - 0.04,
    origen=origen_isla,
    material=mat_madera
)

# --- Mobiliario de la isla ---
A.crear_mesa(
    nombre="MesitaIsla",
    ancho=0.6,
    fondo=0.4,
    alto=0.75,
    origen=(ancho_isla - 0.6/2, fondo_isla - 0.4/2, 0),
    material_tablero=mat_madera,
    material_patas=mat_metal
)

A.crear_mesa(
    nombre="MesitaIsla2",
    ancho=0.6,
    fondo=0.4,
    alto=0.75,
    origen=(ancho_isla - 0.6/2, fondo_isla + 0.4/2, 0),
    material_tablero=mat_madera,
    material_patas=mat_metal
)

# --- Iluminación y cámara ---
A.agregar_luz(
    nombre="LuzPrincipal",
    tipo="AREA",
    ubicacion=(ancho_total / 2, fondo_total / 2, alto_piso + 2.5),
    energia=800
)
A.crear_camara(
    nombre="CamaraCocina",
    ubicacion=(-3, -4, 3),
    rotacion=(70, 0, 0),
    activa=True
)