import blender_arch as A

A.limpiar_escena()

# Crear el edificio base
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioConBalcones",
    pisos=5,
    ancho=18.0,
    fondo=14.0,
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

# Crear balcón en voladizo
def crear_balcon_voladizo(piso):
    # Calcular posición del balcón
    pos_x = -18.0 / 2 + 0.25 + (ancho_balcon / 2)
    pos_y = -14.0 / 2 + 0.25 + (fondo_balcon / 2)
    
    # Crear el balcón en el mismo origen que el piso
    A.crear_losa_rectangular(
        nombre=f"Balcon_{piso}",
        ancho=ancho_balcon,
        fondo=fondo_balcon,
        espesor=0.2,
        origen=(pos_x, pos_y, piso * 3),
        material="Madera_Roble"
    )
    
    # Crear baranda
    altura_total = alto_baranda + 0.2 # 0.2 de espesor
    pos_z_baranda = piso * 3 + alto_baranda
    
    A.crear_losa_rectangular(
        nombre=f"Baranda_{piso}",
        ancho=ancho_balcon,
        fondo=fondo_balcon,
        espesor=0.1,
        origen=(pos_x, pos_y, pos_z_baranda),
        material="Acero_Inox"
    )

# Aplicar la función a cada piso
for i in range(1, 6):
    crear_balcon_voladizo(i)