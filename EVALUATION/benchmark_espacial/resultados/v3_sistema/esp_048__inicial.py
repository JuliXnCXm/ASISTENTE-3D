import blender_arch as A

A.limpiar_escena()

# Edificio tipo Oficina
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Oficina",
    pisos=6,
    ancho=10.0,
    fondo=12.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_muro="Ladrillo"
)

# Balcones en fachada Este
for i in range(1, 7):
    # Calcular posición de cada balcón
    x_pos = 0.1 + (i * 10.0) - 1.5 / 2
    y_pos = 0.1
    
    # Crear balcón
    A.crear_losa_rectangular(
        nombre=f"Balcon_{i}",
        ancho=3.0,
        fondo=1.5,
        espesor=0.2,
        origen=(x_pos, y_pos, i * 3.0),
        material="Hormigon"
    )
    
    # Baranda sobre el balcón
    A.crear_baranda_lineal(
        nombre=f"Baranda_Balcon_{i}",
        largo=3.0,
        altura=0.9,
        poste_cada=1.0,
        origen=(x_pos, y_pos, i * 3.0 + 0.2),
        material="Acero_Inox"
    )