import blender_arch as A
A.limpiar_escena()

# Edificio de oficinas contemporáneo
edificio = A.crear_edificio_n_pisos(
    nombre="Edificio_Oficinas",
    pisos=2,
    ancho=10.0,
    fondo=12.0,
    alto_piso=3.2,
    grosor_muro=0.25,
    con_techo_plano=True,
    con_columnas=False,
    material_muro="Estuco",
    material_losa="Hormigon",
    material_vidrio="Vidrio_Templado",
    material_marco="Marco_Aluminio",
    material_celosia="Madera_Roble",
    material_tejado="Teja"
)

# Entrada principal en la cara frontal
A.crear_ventana("Entrada_Principal", ancho=2.0, alto=2.2, prof_marco=0.2, origen=(4.0, 0, 0), material_marco="Marco_Negro", material_vidrio="Vidrio_Templado")

# Vano para la entrada en la planta baja
A.abrir_vanos_batch_rectangulares(edificio, centros_world=[(4.0, 0, 0.8)], ancho=2.0, alto=2.2)