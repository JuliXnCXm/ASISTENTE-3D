import blender_arch as A

A.limpiar_escena()

# --- Parámetros ---
ancho_total = 6.0
fondo_total = 9.2
alto_piso = 2.8
grosor_muro = 0.15

# --- Materiales ---
mat_muro = "Muro_Pintura"
mat_suelo = "Parquet"
mat_techo = "Yeso"
mat_marco = "Marco_Blanco"

# --- Estructura ---
piso = A.crear_losa_rectangular("PisoGeneral", ancho=ancho_total, fondo=fondo_total, espesor=0.2, origen=(0, 0, -0.2), material=mat_suelo)
techo = A.crear_techo_plano("TechoGeneral", ancho=ancho_total, fondo=fondo_total, espesor=0.2, origen=(0, 0, alto_piso), material=mat_techo)

# --- Muros Perimetrales ---
muro_frente = A.crear_muro("MuroFrente", largo=ancho_total, alto=alto_piso, grosor=grosor_muro, origen=(-ancho_total/2, -fondo_total/2, 0), material=mat_muro)
muro_fondo = A.crear_muro("MuroFondo", largo=ancho_total, alto=alto_piso, grosor=grosor_muro, origen=(-ancho_total/2, fondo_total/2, 0), material=mat_muro)
muro_izq = A.crear_muro("MuroIzq", largo=fondo_total, alto=alto_piso, grosor=grosor_muro, origen=(-ancho_total/2, -fondo_total/2, 0), rotacion_z=90, material=mat_muro)
muro_der = A.crear_muro("MuroDer", largo=fondo_total, alto=alto_piso, grosor=grosor_muro, origen=(ancho_total/2, -fondo_total/2, 0), rotacion_z=90, material=mat_muro)

# --- Muros Interiores ---
# Separación zona día/noche
muro_div_dorm = A.crear_muro("MuroDivDorm", largo=4.0, alto=alto_piso, grosor=grosor_muro, origen=(0, -3.6, 0), material=mat_muro)
# Separación zona privada (dormitorio)
muro_div_banos = A.crear_muro("MuroDivBanos", largo=3.0, alto=alto_piso, grosor=grosor_muro, origen=(0, -3.6, 0), rotacion_z=90, material=mat_muro)
# Muro baño
muro_bano_1 = A.crear_muro("MuroBano1", largo=2.0, alto=alto_piso, grosor=grosor_muro, origen=(-3.0, -1.6, 0), material=mat_muro)
muro_bano_2 = A.crear_muro("MuroBano2", largo=1.0, alto=alto_piso, grosor=grosor_muro, origen=(-3.0, -3.6, 0), rotacion_z=90, material=mat_muro)

# --- Mobiliario ---
# Zona día
sofa = A.crear_sofa("Sofa", ancho=2.2, fondo=0.9, origen=(-2.5, -1.5, 0), material="Tela_Gris")
mesa_comedor = A.crear_mesa("MesaComedor", ancho=1.8, fondo=0.9, origen=(1.0, -1.5, 0), material_tablero="Madera_Roble")
silla1 = A.crear_silla("Silla1", origen=(0.5, -1.5, 0))
silla2 = A.crear_silla("Silla2", origen=(1.5, -1.5, 0))
silla3 = A.crear_silla("Silla3", origen=(2.5, -1.5, 0))
silla4 = A.crear_silla("Silla4", origen=(0.5, -2.5, 0))
silla5 = A.crear_silla("Silla5", origen=(1.5, -2.5, 0))
silla6 = A.crear_silla("Silla6", origen=(2.5, -2.5, 0))

# Cocina
encimera = A.crear_mesa("EncimeraCocina", ancho=2.5, fondo=0.6, alto=0.9, origen=(1.0, -4.0, 0), material_tablero="Acero_Inox")

# Dormitorio
cama = A.crear_cama("CamaPrincipal", ancho=1.6, largo=2.0, origen=(1.2, -1.0, 0), material_colchon="Textil_Blanco", material_base="Madera_Nogal")
armario = A.crear_armario("ArmarioDorm", ancho=2.0, alto=alto_piso, fondo=0.6, origen=(1.0, -3.6 + 0.3, 0), material_cuerpo="MDF_Blanco")

# --- Huecos ---
puerta_entrada = A.crear_puerta("PuertaEntrada", ancho=0.9, alto=2.1, origen=(-ancho_total/2 + 0.45, -fondo_total/2, 0), material_panel="Madera", material_marco=mat_marco)
ventana_sala = A.crear_ventana("VentanaSala", ancho=2.5, alto=1.5, origen=(-1.25, -fondo_total/2, 1.0), material_marco=mat_marco)
ventana_dorm = A.crear_ventana("VentanaDorm", ancho=1.5, alto=1.2, origen=(0, -1.5, 1.6), material_marco=mat_marco)
ventana_bano = A.crear_ventana("VentanaBano", ancho=1.0, alto=1.0, origen=(-3.0, -3.6, 1.5), material_marco=mat_marco)

# --- Iluminación y Cámara ---
A.agregar_luz("LuzPrincipal", tipo="AREA", ubicacion=(0, 0, alto_piso+2), energia=800, color=(1, 0.95, 0.9))
A.crear_camara("CamaraVivienda", ubicacion=(-4, -5, 4), rotacion=(70, 0, -30), activa=True)