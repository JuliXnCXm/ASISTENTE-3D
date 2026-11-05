import blender_arch as A
A.limpiar_escena()

# --- Parámetros ---
ancho_total = 7.0
fondo_total = 8.0
alto_piso = 2.8

# --- Estructura y Pisos ---
A.crear_habitacion(
    nombre="SalaComedor",
    ancho=4.0,
    fondo=5.0,
    alto=alto_piso,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)
A.crear_habitacion(
    nombre="Dormitorio",
    ancho=3.0,
    fondo=4.0,
    alto=alto_piso,
    origen=(ancho_total - 3.0, 0, 0),
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# --- Muebles y Barra ---
A.crear_mesa(
    nombre="BarraCocina",
    ancho=1.2,
    fondo=0.6,
    alto=0.9,
    origen=(ancho_total - 0.6, 1.5, 0),
    material_tablero="Madera_Roble"
)
A.crear_armario(
    nombre="ArmarioDormitorio",
    ancho=2.5,
    alto=2.4,
    fondo=0.6,
    num_puertas=3,
    origen=(ancho_total - 2.5, 0.2, 0),
    material_cuerpo="MDF_Blanco"
)

# --- Ventanas ---
A.crear_ventana(
    nombre="VentanaSala",
    ancho=2.0,
    alto=1.2,
    prof_marco=0.2,
    origen=(ancho_total - 2.0, 1.0, 1.1),
    material_marco="Marco_Aluminio",
    material_vidrio="Vidrio"
)
A.crear_ventana(
    nombre="VentanaDormitorio",
    ancho=1.8,
    alto=1.2,
    prof_marco=0.2,
    origen=(ancho_total - 1.8, 0.2, 1.1),
    material_marco="Marco_Aluminio",
    material_vidrio="Vidrio"
)