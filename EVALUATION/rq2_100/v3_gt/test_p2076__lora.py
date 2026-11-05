import blender_arch as A

A.limpiar_escena()

# Crear la estructura de la habitación
A.crear_habitacion(
    nombre="Sala_Estar",
    ancho=4.0,
    fondo=5.0,
    alto=2.8,
    material_muro="Muro_Pintura_Gris",
    material_suelo="Parquet"
)

# Colocar un sofá contra la pared del fondo
A.crear_sofa(
    nombre="Sofa_Principal",
    ancho=2.2,
    origen=(1.4, 4.5, 0),
    material="Tela_Beige"
)

# Colocar una alfombra centrada sobre el suelo
A.crear_alfombra(
    nombre="Alfombra_Sala",
    ancho=2.5,
    fondo=1.8,
    origen=(1.75, 2.5, 0),
    material="Textil_Blanco"
)

# Crear y posicionar estanterías a lo largo de las paredes
estanterias = []
for i in range(4):
    # Calcular la posición de cada estantería
    x_pos = 0.1 + i * (4.0 - 0.2) / 3
    y_pos = 0.1 if i % 2 == 0 else 4.9
    z_pos = 0.2
    
    # Crear la estantería en la posición calculada
    estanteria = A.crear_estanteria(
        nombre=f"Estanteria_{i+1}",
        ancho=0.8,
        alto=2.2,
        fondo=0.3,
        num_estantes=5,
        origen=(x_pos, y_pos, z_pos),
        material="Madera_Roble"
    )
    estanterias.append(estanteria)

# Aplicar una ligera escala global para que todo encaje mejor
A.escalar_escena(0.95)