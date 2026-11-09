import blender_arch as A

A.limpiar_escena()

# Crear el edificio base
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioConBalcones",
    pisos=3,
    ancho=20.0,
    fondo=10.0,
    alto_piso=3.0,
    grosor_muro=0.25,
    con_techo_plano=True,
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon"
)

# Definir parámetros del balcón
ancho_balcon = 3.0
fondo_balcon = 1.5
alto_baranda = 1.0

# Calcular posiciones de los balcones
num_pisos = 3
pos_y_fachada = 10.0 / 2 - 0.1 # Centrar en la fachada
pos_z_piso = [i * 3.0 for i in range(1, num_pisos + 1)]

for i, z_piso in enumerate(pos_z_piso):
    # Calcular posición del balcón en el piso actual
    pos_x_balcon = (ancho_balcon / 2) - 0.1 # Centrar en el muro
    pos_y_balcon = pos_y_fachada
    
    # Crear el balcón
    A.crear_losa_rectangular(
        nombre=f"Balcon_{i+1}",
        ancho=ancho_balcon,
        fondo=fondo_balcon,
        espesor=0.2,
        origen=(pos_x_balcon, pos_y_balcon, z_piso),
        material="Hormigon"
    )
    
    # Crear la baranda sobre el balcón
    altura_total_balcon = alto_baranda + 0.2 # 0.2m de soporte
    pos_z_baranda = z_piso + (alto_baranda / 2)
    
    A.crear_losa_rectangular(
        nombre=f"Baranda_{i+1}",
        ancho=ancho_balcon,
        fondo=fondo_balcon,
        espesor=0.1,
        origen=(pos_x_balcon, pos_y_balcon, pos_z_baranda),
        material="Acero_Inox"
    )