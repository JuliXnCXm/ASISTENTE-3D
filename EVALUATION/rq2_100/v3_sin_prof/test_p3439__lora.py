import blender_arch as A
A.limpiar_escena()

# Crear la estructura de la oficina
oficina = A.crear_habitacion(
    nombre="OficinaOpenPlan",
    ancho=8.0,
    fondo=6.0,
    alto=3.0,
    grosor_muro=0.2,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Zona de trabajo principal
A.crear_mesa(nombre="Escritorio1", ancho=1.4, fondo=0.7, alto=0.75, origen=(1.5, 1.5, 0), material_tablero="Madera_Roble")
A.crear_silla(nombre="Silla1", origen=(1.5, 2.2, 0), material="Cuero")

A.crear_mesa(nombre="Escritorio2", ancho=1.4, fondo=0.7, alto=0.75, origen=(6.5, 1.5, 0), material_tablero="Madera_Roble")
A.crear_silla(nombre="Silla2", origen=(6.5, 2.2, 0), material="Cuero")

A.crear_mesa(nombre="Escritorio3", ancho=1.4, fondo=0.7, alto=0.75, origen=(1.5, 4.5, 0), material_tablero="Madera_Roble")
A.crear_silla(nombre="Silla3", origen=(1.5, 5.2, 0), material="Cuero")

A.crear_mesa(nombre="Escritorio4", ancho=1.4, fondo=0.7, alto=0.75, origen=(6.5, 4.5, 0), material_tablero="Madera_Roble")
A.crear_silla(nombre="Silla4", origen=(6.5, 5.2, 0), material="Cuero")

# Sala de reuniones en una esquina
sala = A.crear_habitacion(
    nombre="SalaReuniones",
    ancho=3.0,
    fondo=3.0,
    alto=3.0,
    grosor_muro=0.2,
    origen=(5.0, 3.0, 0),
    material_muro="Vidrio_Templado",
    material_suelo="Ceramica_Piso"
)
A.crear_mesa(nombre="MesaReunion", ancho=1.8, fondo=1.8, alto=0.75, origen=(1.1, 1.1, 0), material_tablero="Madera_Roble")
A.crear_silla(nombre="SillaReunion1", origen=(0.9, 1.9, 0), material="Cuero")
A.crear_silla(nombre="SillaReunion2", origen=(2.3, 1.9, 0), material="Cuero")
A.crear_silla(nombre="SillaReunion3", origen=(1.9, 0.9, 0), material="Cuero")
A.crear_silla(nombre="SillaReunion4", origen=(1.9, 2.3, 0), material="Cuero")