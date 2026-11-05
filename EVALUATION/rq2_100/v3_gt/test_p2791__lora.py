import blender_arch as A

A.limpiar_escena()

# Crear la fachada principal
fachada = A.crear_muro(
    nombre="Fachada_Principal",
    largo=10.0,
    alto=6.0,
    grosor=0.3,
    material="Muro_Pintura_Gris"
)

# Definir parámetros de la retícula de ventanas
ancho_fachada = 10.0
alto_piso = 3.0
num_ventanas_x = 4
num_ventanas_y = 2

# Calcular dimensiones y posición de las ventanas
ancho_vano = ancho_fachada / num_ventanas_x
alto_vano = alto_piso / num_ventanas_y
pos_x_base = ancho_vano / 2
pos_y_base = alto_piso / 2

# Crear y posicionar las ventanas
for i in range(num_ventanas_x):
    for j in range(num_ventanas_y):
        # Calcular posición de cada vano
        x = pos_x_base + i * ancho_vano
        y = pos_y_base + j * alto_vano
        
        # Abrir el vano en la fachada
        A.abrir_vanos_batch_rectangulares(
            muro=fachada,
            centros_world=[(x, y, alto_piso / 2)],
            ancho=ancho_vano,
            alto=alto_vano
        )