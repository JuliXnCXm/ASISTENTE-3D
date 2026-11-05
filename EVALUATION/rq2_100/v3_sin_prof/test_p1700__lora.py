import blender_arch as A
A.limpiar_escena()

# Base de la acera
A.crear_terreno_plano(
    nombre="Acera",
    ancho=18,
    fondo=18,
    espesor=0.15,
    origen=(0, 0, -0.15),
    material="Concreto_Piso"
)

# Edificio de oficinas
A.crear_edificio_n_pisos(
    nombre="Edificio_Oficinas",
    pisos=5,
    ancho=12.0,
    fondo=9.0,
    alto_piso=3.2,
    grosor_muro=0.3,
    con_techo_plano=True,
    con_columnas=True,
    dim_columna=0.4,
    modulo_columna_x=4.0,
    modulo_columna_y=5.0,
    ventanas_fachada=True,
    ventana_ancho=1.5,
    ventana_alto=1.8,
    ventana_alfeizar=1.0,
    ventana_separacion=3.0,
    origen=(0, 0, 0),
    material_fachada="Muro_Pintura_Gris",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio"
)