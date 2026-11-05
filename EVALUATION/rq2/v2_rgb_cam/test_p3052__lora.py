import blender_arch as A

A.limpiar_escena()

# --- ESTRUCTURA Y ZONA COMÚN ---
A.crear_habitacion(
    nombre="ZonaDía", 
    ancho=6.0, 
    fondo=5.0, 
    alto=2.8, 
    grosor_muro=0.15, 
    material_muro="Muro_Pintura_Gris", 
    material_suelo="Porcelanato"
)
A.crear_techo_plano("Techo_ZonaDía", ancho=6.0, fondo=5.0, espesor=0.2, origen=(0,0,2.8), material="Yeso")

# --- MUEBLES ESPECÍFICOS ---
A.crear_mesa("MesaComedor", ancho=1.8, fondo=0.9, alto=0.75, origen=(1.5, 3.5, 0), material_tablero="Madera_Roble")
A.crear_sofa("SofaPrincipal", ancho=2.2, fondo=0.9, origen=(1.5, 1.5, 0), material="Tela_Gris")

# --- BAÑO ---
A.crear_habitacion("Baño", ancho=2.5, fondo=2.0, alto=2.8, grosor_muro=0.15, origen=(3.5, 0, 0), material_muro="Muro_Pintura_Gris", material_suelo="Ceramica_Piso")
A.crear_puerta("PuertaBaño", ancho=0.8, alto=2.1, origen=(3.5 + 0.15, 0.1, 0), material_panel="Madera_Nogal", material_marco="Marco_Blanco")

# --- DORMITORIO ---
A.crear_habitacion("Dormitorio", ancho=3.0, fondo=4.0, alto=2.8, grosor_muro=0.15, origen=(-1.5, -1.5, 0), material_muro="Muro_Pintura_Gris", material_suelo="Parquet")
A.crear_cama("CamaDormitorio", ancho=1.6, largo=2.0, origen=(0, -1.5, 0), material_base="Madera_Roble", material_colchon="Textil_Blanco")
A.crear_armario("ArmarioDormitorio", ancho=1.8, alto=2.4, fondo=0.6, origen=(-1.5, -1.5, 0), material_cuerpo="MDF_Blanco")

# --- ILUMINACIÓN Y CÁMARA ---
A.agregar_luz("LuzGeneral", tipo="AREA", ubicacion=(0, 0, 3.0), energia=250, color=(1, 0.95, 0.85))
A.crear_camara("CamaraInterior", ubicacion=(0, -6, 1.5), rotacion=(80, 0, 0), activa=True)