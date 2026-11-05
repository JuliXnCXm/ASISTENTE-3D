import blender_arch as A

A.limpiar_escena()

# --- ESTRUCTURA Y ZONAS ---
ancho_total = 6.0
fondo_total = 9.0
alto_piso = 2.8
grosor_muro = 0.2

# Crear el espacio base
A.crear_habitacion(
    nombre="ZonaDía", 
    ancho=ancho_total, 
    fondo=fondo_total, 
    alto=alto_piso, 
    grosor_muro=grosor_muro,
    material_muro="Muro_Pintura",
    material_suelo="Porcelanato"
)

# --- MOBILIARIO ZONA DÍA (SALA-COMEDOR) ---
# Sofá contra la pared del fondo
sofa = A.crear_sofa(
    nombre="SofaPrincipal", 
    ancho=2.5, 
    origen=(ancho_total/2, fondo_total - 0.2 - 0.1, 0), 
    material="Tela_Gris"
)
# Mesa de centro frente al sofá
mesa_centro = A.crear_mesa(
    nombre="MesaCentro", 
    ancho=1.2, 
    fondo=0.6, 
    alto=0.45, 
    origen=(ancho_total/2, 1.5, 0), 
    material_tablero="Madera_Roble"
)

# --- MOBILIARIO ZONA COCINA ---
# Encimera y muebles bajos
encimera_cocina = A.crear_losa_rectangular("EncimeraCocina", ancho=2.5, fondo=0.6, espesor=0.04, origen=(ancho_total/2, 0.2, 0))
mueble_cocina = A.crear_armario("MuebleCocina", ancho=2.5, alto=0.9, fondo=0.6, origen=(ancho_total/2, 0.2, 0), material_cuerpo="MDF_Blanco")
# Encimera alta
encimera_alta = A.crear_losa_rectangular("EncimeraAlta", ancho=2.5, fondo=0.6, espesor=0.04, origen=(ancho_total/2, 0.2 + 0.6 + 0.1, 0))

# --- BAÑO ---
# Mampara de ducha
mampara_ducha = A.crear_muro("MamparaDucha", largo=2.5, alto=2.0, grosor=0.02, origen=(ancho_total/2, 0.2, 0), material="Vidrio_Templado")
# Mampara lavabo
mampara_lavabo = A.crear_muro("MamparaLavabo", largo=2.5, alto=2.0, grosor=0.02, origen=(ancho_total/2, 0.2 + 0.6 + 0.1 + 0.1, 0), material="Vidrio_Templado")

# --- DORMITORIO PRINCIPAL ---
# Muro del dormitorio
muro_dormitorio = A.crear_muro("MuroDormitorio", largo=4.0, alto=2.8, grosor=0.15, origen=(0, 0, 0), material="Muro_Pintura")
# Cabecero y cama
cabecero = A.crear_panel_vano("Cabecero", ancho=1.8, alto=1.2, prof_marco=0.15, origen=(ancho_total/2 - 0.9, 0.2, 0), material_panel="Madera_Nogal", material_marco="Marco_Negro")
cama = A.crear_cama("CamaPrincipal", ancho=1.6, largo=2.0, origen=(ancho_total/2 - 0.8, 0.2, 0), material_colchon="Textil_Blanco", material_base="Madera_Nogal")

# --- ILUMINACIÓN Y CAMARA ---
A.agregar_luz("LuzGeneral", tipo="AREA", ubicacion=(ancho_total/2, fondo_total/2, alto_piso - 0.1), energia=250)
A.crear_camara("CamaraInterior", ubicacion=(ancho_total/2, -5, alto_piso/2), rotacion=(70, 0, 0))