import blender_arch as A

A.limpiar_escena()

# --- ESTRUCTURA Y ZONAS ---
ancho_total = 5.5
fondo_total = 10.0
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
mampara_ducha = A.crear_muro("MamparaDucha", largo=1.5, alto=2.0, grosor=0.01, origen=(ancho_total - 0.2 - 0.1, 0.2, 0), material="Vidrio_Templado")
# Mampara lavabo
mampara_lavabo = A.crear_muro("MamparaLavabo", largo=1.5, alto=2.0, grosor=0.01, origen=(ancho_total - 0.2 - 0.1, 0.2 + 0.6 + 0.1, 0), material="Vidrio_Templado")

# --- DORMITORIO PRINCIPAL ---
# Cabecero y mesita de noche
cabecero = A.crear_losa_rectangular("Cabecero", ancho=1.6, fondo=0.2, espesor=0.2, origen=(ancho_total/2 - 0.8, 0.2, 0), material="Madera_Nogal")
mesita_noche = A.crear_mesa("MesitaNoche", ancho=0.4, fondo=0.4, alto=0.6, origen=(ancho_total/2 - 0.8 - 0.2, 0.2 + 0.2, 0), material_tablero="Madera_Nogal")

# --- ILUMINACIÓN Y CAMARA ---
A.agregar_luz("LuzPrincipal", tipo="AREA", ubicacion=(ancho_total/2, fondo_total/2, alto_piso - 0.1), energia=250)
A.crear_camara("CamaraInterior", ubicacion=(ancho_total/2, -5, alto_piso/2), rotacion=(80, 0, 0))