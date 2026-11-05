import blender_arch as A
A.limpiar_escena()

# Edificio de oficinas con fachada de vidrio
edificio = A.crear_edificio_n_pisos(
    nombre="EdificioApartamentos",
    pisos=5,
    ancho=16.0,
    fondo=8.0,
    alto_piso=3.2,
    grosor_muro=0.3,
    con_techo_plano=True,
    con_columnas=False,
    material_fachada="Estuco",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio"
)

# Crear balcón en la cara frontal
ancho_balcon = 2.0
fondo_balcon = 0.9

for p in range(5):
    # Mover a la posición correcta
    z_pos = p * alto_piso
    
    # Crear balcón
    A.crear_losa_rectangular(
        nombre=f"Balcon_Frente_{p+1}",
        ancho=ancho_balcon,
        fondo=fondo_balcon,
        espesor=0.2,
        origen=(0, -fondo_balcon/2, z_pos),
        material="Concreto_Piso"
    )
    
    # Crear barandilla de vidrio
    A.crear_losa_rectangular(
        nombre=f"Barandilla_Frente_{p+1}",
        ancho=ancho_balcon,
        fondo=0.1,
        espesor=0.02,
        origen=(0, -fondo_balcon/2 + 0.45, z_pos + 0.2),
        material="Vidrio_Templado"
    )

# Crear puerta corredera en la cara frontal
ancho_puerta = 1.8
alto_puerta = 2.2

for p in range(5):
    # Mover a la posición correcta
    z_pos = p * alto_piso
    
    # Crear marco de puerta
    A.crear_losa_rectangular(
        nombre=f"Marco_Puerta_{p+1}",
        ancho=ancho_puerta + 0.2,
        fondo=0.1,
        espesor=0.15,
        origen=(-ancho_balcon/2 + 0.1, -fondo_balcon/2 + 0.45, z_pos),
        material="Marco_Aluminio"
    )
    
    # Crear hoja de puerta
    A.crear_losa_rectangular(
        nombre=f"Hoja_Puerta_{p+1}",
        ancho=ancho_puerta,
        fondo=alto_puerta,
        espesor=0.02,
        origen=(-ancho_balcon/2 + 0.1, -fondo_balcon/2 + 0.45, z_pos),
        material="Vidrio_Templado"
    )