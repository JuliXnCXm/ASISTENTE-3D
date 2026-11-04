import blender_arch as A
import bpy

A.limpiar_escena()

# --- Definir dimensiones y materiales ---
ANCHO_CASA = 5.5
FONDO_CASA = 10.0
ALTO_PISO = 2.8
GROSOR_MURO = 0.2

# --- Crear estructura principal ---
losa = A.crear_losa_rectangular("LosaSuelo", ANCHO_CASA, FONDO_CASA, 0.2, material="Concreto_Piso")
techo = A.crear_techo_plano("Techo", ANCHO_CASA, FONDO_CASA, 0.2, origen=(0, 0, ALTO_PISO), material="Muro_Pintura")

# --- Muros exteriores ---
muro_frente = A.crear_muro("MuroFrente", ANCHO_CASA, ALTO_PISO, GROSOR_MURO, origen=(0, FONDO_CASA - GROSOR_MURO, 0), material="Estuco")
muro_fondo = A.crear_muro("MuroFondo", ANCHO_CASA, ALTO_PISO, GROSOR_MURO, origen=(0, 0, 0), material="Estuco")
muro_izq = A.crear_muro("MuroIzq", FONDO_CASA, ALTO_PISO, GROSOR_MURO, origen=(0, 0, 0), material="Estuco")
muro_der = A.crear_muro("MuroDer", FONDO_CASA, ALTO_PISO, GROSOR_MURO, origen=(ANCHO_CASA - GROSOR_MURO, 0, 0), material="Estuco")

# --- Muros interiores (división zona privada) ---
# Zona privada al fondo (4m de fondo)
muro_div_principal = A.crear_muro("MuroDivPrincipal", ANCHO_CASA - GROSOR_MURO, ALTO_PISO, GROSOR_MURO, origen=(GROSOR_MURO, 4.0, 0), material="Muro_Pintura")

# División entre dormitorio y baño
ancho_bano = 2.0
muro_div_bano = A.crear_muro("MuroDivBano", 4.0, ALTO_PISO, 0.15, origen=(ancho_bano, 0, 0), material="Muro_Pintura")

# --- Vano y Puertas ---
puerta_entrada = A.crear_puerta("PuertaEntrada", 0.9, 2.1, prof_marco=GROSOR_MURO, material_panel="Madera_Roble", material_marco="Marco_Negro")
A.anclar_a(puerta_entrada, muro_frente, "frente", offset=(1.0, 0, 0))
A.abrir_vanos_batch_rectangulares(muro_frente, [puerta_entrada.location], 0.9, 2.1)

puerta_dorm = A.crear_puerta("PuertaDormitorio", 0.8, 2.1, prof_marco=0.15, material_panel="Madera", material_marco="Marco_Blanco")
A.anclar_a(puerta_dorm, muro_div_principal, "frente", offset=(ancho_bano + 1.0, 0, 0))
A.abrir_vanos_batch_rectangulares(muro_div_principal, [puerta_dorm.location], 0.8, 2.1)

puerta_bano = A.crear_puerta("PuertaBaño", 0.7, 2.1, prof_marco=0.15, material_panel="Madera", material_marco="Marco_Blanco")
A.anclar_a(puerta_bano, muro_div_principal, "frente", offset=(ancho_bano/2, 0, 0))
A.abrir_vanos_batch_rectangulares(muro_div_principal, [puerta_bano.location], 0.7, 2.1)

# --- Ventanas ---
ventana_sala = A.crear_ventana("VentanaSala", 2.5, 1.2, prof_marco=GROSOR_MURO, divisiones=(3,1), material_marco="Marco_Negro")
A.anclar_a(ventana_sala, muro_frente, "frente", offset=(ANCHO_CASA/2 + 0.2, 0, 1.0))
A.abrir_vanos_batch_rectangulares(muro_frente, [ventana_sala.location], 2.5, 1.2)

ventana_dorm = A.crear_ventana("VentanaDormitorio", 1.5, 1.2, prof_marco=GROSOR_MURO, divisiones=(2,1), material_marco="Marco_Negro")
A.anclar_a(ventana_dorm, muro_fondo, "frente", offset=(ancho_bano + (ANCHO_CASA - ancho_bano)/2, 0, 1.0))
A.abrir_vanos_batch_rectangulares(muro_fondo, [ventana_dorm.location], 1.5, 1.2)


# --- Mobiliario ---
# Cocina (L: 3m, F: 0.6m, A: 0.9m)
mesada_cocina = A.extruir_perfil("MesadaCocina", [(0,0), (3.0,0), (3.0,0.6), (0,0.6)], altura=0.9, material="MDF_Blanco")
mesada_cocina.location = (GROSOR_MURO + 0.1, FONDO_CASA - GROSOR_MURO - 3.0, 0)
mesada_cocina.rotation_euler[2] = 1.5708 # 90 deg

# Sala-Comedor
sofa = A.crear_sofa("Sofa", ancho=2.0, origen=(ANCHO_CASA - GROSOR_MURO - 2.2, FONDO_CASA - GROSOR_MURO - 1.2, 0.2), material="Tela_Gris")
sofa.rotation_euler[2] = -1.5708

mesa = A.crear_mesa("MesaComedor", ancho=1.2, fondo=0.8, origen=(1.5, 6.0, 0.2), material_tablero="Madera")
silla1 = A.crear_silla("Silla1", origen=(1.5, 5.5, 0.2), material="Madera")
silla2 = A.crear_silla("Silla2", origen=(1.5, 6.5, 0.2), material="Madera")
silla2.rotation_euler[2] = 3.14159

# Dormitorio
cama = A.crear_cama("CamaPrincipal", ancho=1.6, origen=(ancho_bano + 0.5, 0.2, 0.2), material_colchon="Textil_Blanco", material_base="Madera_Roble")
armario = A.crear_armario("ArmarioDorm", ancho=1.8, origen=(ancho_bano + 0.3, 4.0 - GROSOR_MURO - 0.6, 0.2), material_cuerpo="MDF_Blanco")
armario.rotation_euler[2] = 3.14159

# --- Iluminación y Cámara ---
A.agregar_luz("LuzPrincipal", tipo='SUN', ubicacion=(10, -10, 15), energia=2.0)
A.crear_camara("CamaraPrincipal", ubicacion=(10, 15, 8), rotacion=(60, 0, 30), activa=True)