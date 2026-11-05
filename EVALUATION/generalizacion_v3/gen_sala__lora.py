import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la habitación
habitacion = A.crear_habitacion(
    nombre="SalaDeEstar",
    ancho=6.0,
    fondo=5.0,
    alto=2.8,
    material_muro="Estuco",
    material_suelo="Parquet"
)

# Colocar mobiliario
sofa = A.crear_sofa(
    nombre="SofaPrincipal",
    ancho=2.4,
    origen=(1.8, 0.3, 0),
    material="Tela_Gris"
)
mesa_centro = A.crear_mesa(
    nombre="MesaCentro",
    ancho=1.2,
    fondo=0.6,
    alto=0.45,
    origen=(2.4, 2.0, 0),
    material_tablero="Madera_Roble"
)
silla_1 = A.crear_silla(nombre="Silla1", origen=(0.9, 2.0, 0), material="Cuero")
silla_2 = A.crear_silla(nombre="Silla2", origen=(4.5, 2.0, 0), material="Cuero")

# Crear y posicionar la ventana
ventana_ancho = 3.0
ventana_alto = 1.5
ventana_origen = (1.5, 0.1, 1.1)
A.crear_ventana(
    nombre="VentanaPrincipal",
    ancho=ventana_ancho,
    alto=ventana_alto,
    prof_marco=0.1,
    origen=ventana_origen,
    material_marco="Marco_Blanco",
    material_vidrio="Vidrio"
)