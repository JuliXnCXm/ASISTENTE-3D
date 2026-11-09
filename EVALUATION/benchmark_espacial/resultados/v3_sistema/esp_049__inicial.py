import blender_arch as A

A.limpiar_escena()

# Crear el edificio base
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioOficinas",
    pisos=6,
    ancho=12.0,
    fondo=12.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_marco="Marco_Negro",
    material_vidrio="Vidrio"
)

# Añadir balcón en voladizo a la fachada sur (Y+)
for i in range(1, 7): # Pisos 1-6
    x_pos = -12.0 / 2 + 0.25 # Centrado en Y
    z_pos = i * 3.0 # Altura del piso actual
    
    A.crear_losa_rectangular(
        nombre=f"Balcon_{i}",
        ancho=12.0,
        fondo=1.5,
        espesor=0.2,
        origen=(x_pos, 12.0 / 2 - 0.25, z_pos),
        material="Hormigon"
    )
    
    A.crear_baranda_lineal(
        nombre=f"Baranda_{i}",
        largo=12.0,
        altura=0.9,
        poste_cada=1.2,
        origen=(x_pos, 12.0 / 2 - 0.25, z_pos + 0.2),
        material="Acero_Inox"
    )