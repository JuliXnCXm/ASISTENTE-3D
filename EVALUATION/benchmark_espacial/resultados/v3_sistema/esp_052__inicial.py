import blender_arch as A

A.limpiar_escena()

# Edificio tipo Casa con parámetros modificados
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioConBalcones",
    pisos=3,
    ancho=12.0,
    fondo=14.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    con_columnas=False,
    origen=(0, 0, 0),
    material_muro="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Balcón en voladizo en el lado este (Y+)
for i in range(1, 4): # Pisos 1 a 3
    # Calcular posición del balcón para que quede en el borde este
    pos_x = -12.0 / 2 + 0.15 # 0.15m de contrahuella
    pos_y = 14.0 / 2 - 0.75 # 0.75m de balaustrada
    pos_z = i * 3.0
    
    # Crear balcón
    A.crear_losa_rectangular(
        nombre=f"Balcon_{i}",
        ancho=3.0,
        fondo=1.5,
        espesor=0.2,
        origen=(pos_x, pos_y, pos_z),
        material="Madera_Roble"
    )
    
    # Baranda en el borde frontal
    A.crear_baranda_lineal(
        nombre=f"Baranda_{i}",
        largo=3.0,
        altura=0.9,
        poste_cada=1.0,
        origen=(pos_x, pos_y, pos_z + 0.2),
        material="Acero_Inox"
    )