import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la habitación
habitacion = A.crear_habitacion(
    nombre="OficinaCasa",
    ancho=4.0,
    fondo=3.5,
    alto=2.8,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Crear y posicionar el escritorio de esquina
escritorio = A.crear_mesa(
    nombre="EscritorioEsquina",
    ancho=1.4,
    fondo=0.7,
    alto=0.75,
    origen=(1.3, 0.15, 0),
    material_tablero="Madera_Roble"
)
A.asignar_material(escritorio.children[0], nombre="Madera_Roble")

# Crear y posicionar la silla
silla = A.crear_silla(
    nombre="SillaOficina",
    origen=(1.3 + 0.6/2 - 0.05, 0.15 + 0.4/2, 0),
    material="Cuero"
)

# Crear la librería paramétrica
def crear_estanteria_parametrica(nombre, ancho_total, alto_total, num_estantes, origen):
    # Parámetros de la librería
    ancho_parcial = ancho_total / num_estantes
    alto_parcial = alto_total / (num_estantes - 1)
    
    # Crear estantes individuales
    for i in range(num_estantes):
        x_pos = i * ancho_parcial
        z_pos = (i * alto_parcial) + (alto_parcial / 2)
        
        # El primer estante va contra la pared, el último contra la otra
        if i == 0:
            z_pos = alto_parcial
        elif i == num_estantes - 1:
            z_pos = alto_parcial * (num_estantes - 1)
        
        estante = A.crear_mesa(
            nombre=f"Estante_{i+1}",
            ancho=ancho_parcial,
            fondo=0.3,
            alto=alto_parcial,
            origen=(x_pos, 0.15, z_pos),
            material_tablero="MDF_Blanco"
        )
        A.asignar_material(estante.children[0], nombre="MDF_Blanco")

# Crear la librería en la pared trasera
crear_estanteria_parametrica("LibreriaOficina", 1.8, 2.2, 9, (0, 1.5, 0))