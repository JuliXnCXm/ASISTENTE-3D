import blender_arch as A

A.limpiar_escena()

# Edificio de oficinas con balcones en fachada trasera
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioOficinas",
    pisos=6,
    ancho=16.0,
    fondo=10.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    con_columnas=False,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio"
)

# Balcones en fachada trasera (Y negativo)
for i in range(1, 7):
    # Calcular posición del balcón para que quede en el borde exterior
    pos_x = -16.0 / 2 + 0.25 + 1.5 / 2
    pos_y = -10.0 / 2 + 0.25 + 3.0 * i + 1.5 / 2
    
    # Crear balcón
    A.crear_losa_rectangular(
        nombre=f"Balcon_Fachada_{i}",
        ancho=16.0,
        fondo=1.5,
        espesor=0.2,
        origen=(pos_x, pos_y, 3.0 * i),
        material="Hormigon"
    )
    
    # Baranda en el borde frontal del balcón
    A.crear_losa_rectangular(
        nombre=f"Baranda_Balcon_{i}",
        ancho=16.0,
        fondo=0.15,
        espesor=0.05,
        origen=(pos_x, pos_y, 3.0 * i + 1.5),
        material="Acero_Inox"
    )