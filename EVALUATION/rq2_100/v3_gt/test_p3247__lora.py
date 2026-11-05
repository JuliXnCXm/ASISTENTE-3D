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
    material_suelo="Parquet"
)

# Entrada acristalada en la planta baja
A.crear_ventana("Entrada_Principal", ancho=3.0, alto=2.8, prof_marco=0.2, origen=(3.5, 0.1, 0), material="Vidrio_Templado")
A.abrir_vanos_batch_rectangulares(edificio["Pisos"][0], [(3.5, 0.1, 0)], ancho=3.0, alto=2.8)

# Cubierta con celosía
celosia = A.crear_losa_rectangular("Celosia_Cubierta", ancho=10.0, fondo=12.0, espesor=0.2, origen=(0, 0, 6.4), material="Madera_Roble")