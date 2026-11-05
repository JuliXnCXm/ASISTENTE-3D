import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la cocina
A.crear_habitacion(
    nombre="Cocina",
    ancho=4.0,
    fondo=3.0,
    alto=2.8,
    grosor_muro=0.15,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Porcelanato"
)

# Crear el mobiliario de la cocina
A.crear_mesa(
    nombre="Meson_Cocina",
    ancho=2.5,
    fondo=0.6,
    alto=0.9,
    origen=(1.25, 0.7, 0),
    material_tablero="MDF_Blanco"
)
A.crear_mesa(
    nombre="Encimera_Larga",
    ancho=1.5,
    fondo=0.6,
    alto=0.9,
    origen=(2.5, 1.2, 0),
    material_tablero="MDF_Blanco"
)

# Crear mobiliario auxiliar
A.crear_armario(
    nombre="Armario_Cocina",
    ancho=1.2,
    alto=2.4,
    fondo=0.6,
    num_puertas=3,
    origen=(0.15, 0.6, 0),
    material_cuerpo="MDF_Blanco"
)
A.crear_armario(
    nombre="Armario_Piso",
    ancho=1.2,
    alto=0.9,
    fondo=0.6,
    num_puertas=3,
    origen=(0.15, 1.8, 0),
    material_cuerpo="MDF_Blanco"
)

# Crear mobiliario de comedor
A.crear_mesa(
    nombre="Mesa_Comedor",
    ancho=1.4,
    fondo=0.8,
    alto=0.75,
    origen=(1.8, 2.2, 0),
    material_tablero="Madera_Roble"
)
for i in range(4):
    A.crear_silla(
        nombre=f"Silla_{i+1}",
        origen=(1.8 + 0.3 + i * 0.4, 2.2 - 0.3, 0),
        material="Madera_Roble"
    )

# Crear y colocar una ventana
A.crear_ventana(
    nombre="Ventana_Cocina",
    ancho=1.5,
    alto=1.2,
    prof_marco=0.15,
    origen=(1.25, 0.15, 1.1),
    material_marco="Marco_Negro",
    material_vidrio="Vidrio"
)