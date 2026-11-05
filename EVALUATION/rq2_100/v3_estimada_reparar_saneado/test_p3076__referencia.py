import blender_arch as A
import bpy

A.limpiar_escena()

# --- PARÁMETROS GENERALES ---
ancho_total = 8.0
fondo_total = 9.0
alto_muro = 2.8
grosor_muro = 0.15

# --- MUROS PERIMETRALES ---
muro_frente = A.crear_muro("MuroFrente", ancho_total, alto_muro, grosor_muro, origen=(0, 0, 0), material="Muro_Pintura")
muro_fondo = A.crear_muro("MuroFondo", ancho_total, alto_muro, grosor_muro, origen=(0, fondo_total, 0), material="Muro_Pintura")
muro_izq = A.crear_muro("MuroIzq", fondo_total, alto_muro, grosor_muro, origen=(0, 0, 0), material="Muro_Pintura")
muro_der = A.crear_muro("MuroDer", fondo_total, alto_muro, grosor_muro, origen=(ancho_total, 0, 0), material="Muro_Pintura")

# --- SUELO ---
suelo = A.crear_piso("SueloGeneral", ancho_total, fondo_total, 0.02, origen=(0, 0, 0), material="Parquet")

# --- DISTRIBUCIÓN INTERIOR ---
# Muro separación zona social/privada
muro_pasillo_1 = A.crear_muro("MuroPasillo1", 4.5, alto_muro, grosor_muro, origen=(ancho_total - 4.5, 0, 0))

# Muros Dormitorio Principal y Baño Suite
muro_dorm_ppal_1 = A.crear_muro("MuroDormPpal1", 3.5, alto_muro, grosor_muro, origen=(ancho_total - 4.5, 5.0, 0))
muro_baño_suite = A.crear_muro("MuroBañoSuite", 2.0, alto_muro, grosor_muro, origen=(ancho_total - 2.5, 5.0, 0))

# Muros Dormitorio Secundario y Baño General
muro_dorm_sec = A.crear_muro("MuroDormSec", 3.5, alto_muro, grosor_muro, origen=(0, 5.5, 0))
muro_baño_gen = A.crear_muro("MuroBañoGen", 2.5, alto_muro, grosor_muro, origen=(ancho_total - 4.5, 2.5, 0))

# --- MOBILIARIO ---
# Sala-Comedor
sofa = A.crear_sofa("Sofa", ancho=2.5, fondo=0.9, origen=(0.2, 2.5, 0), material="Tela_Gris")
mesa_comedor = A.crear_mesa("MesaComedor", ancho=1.8, fondo=0.9, alto=0.75, origen=(0.8, 6.5, 0), material_tablero="Madera_Roble")
for i in range(4):
    A.crear_silla(f"Silla.{i}", origen=(1.0 + i*0.6, 5.9, 0), material="Madera_Roble")

# Cocina
cocina_l1 = A.crear_mesa("Encimera1", ancho=3.0, fondo=0.6, alto=0.9, origen=(ancho_total-3.0-0.1, 0.1, 0), material_tablero="MDF_Blanco")
cocina_l2 = A.crear_mesa("Encimera2", ancho=2.5, fondo=0.6, alto=0.9, origen=(ancho_total-0.6-0.1, 0.1, 0), material_tablero="MDF_Blanco")
cocina_l2.rotation_euler[2] = 1.5708 # 90 degrees

# Dormitorio Principal
cama_ppal = A.crear_cama("CamaPpal", ancho=1.6, largo=2.0, origen=(ancho_total-2.0, fondo_total-2.2, 0), material_colchon="Textil_Blanco")
cama_ppal.rotation_euler[2] = -1.5708
armario_ppal = A.crear_armario("ArmarioPpal", ancho=2.4, alto=2.4, fondo=0.6, origen=(ancho_total-4.4, fondo_total-0.7, 0))

# Dormitorio Secundario
cama_sec = A.crear_cama("CamaSec", ancho=1.0, largo=2.0, origen=(0.2, fondo_total-2.2, 0), material_colchon="Textil_Blanco")
armario_sec = A.crear_armario("ArmarioSec", ancho=1.5, alto=2.4, fondo=0.6, origen=(2.0, fondo_total-0.7, 0))

# --- PUERTAS Y VENTANAS ---
puerta_entrada = A.crear_puerta("PuertaEntrada", ancho=1.0, alto=2.2, origen=(ancho_total - 3.5, 0, 0))
puerta_dorm_ppal = A.crear_puerta("PuertaDormPpal", ancho=0.9, alto=2.2, origen=(ancho_total - 4.5, 4.0, 0))
puerta_dorm_sec = A.crear_puerta("PuertaDormSec", ancho=0.9, alto=2.2, origen=(ancho_total - 5.0, 5.5, 0))
puerta_baño_ppal = A.crear_puerta("PuertaBañoPpal", ancho=0.8, alto=2.2, origen=(ancho_total - 3.5, 5.0, 0))
puerta_baño_gen = A.crear_puerta("PuertaBañoGen", ancho=0.8, alto=2.2, origen=(ancho_total - 4.5, 1.5, 0))

ventana_sala = A.crear_ventana("VentanaSala", ancho=3.0, alto=1.5, origen=(0, 1.5, 1.0))
ventana_dorm_ppal1 = A.crear_ventana("VentanaDormPpal1", ancho=1.8, alto=1.2, origen=(ancho_total, fondo_total-2.0, 1.2))
ventana_dorm_ppal2 = A.crear_ventana("VentanaDormPpal2", ancho=1.8, alto=1.2, origen=(ancho_total-2.5, fondo_total, 1.2))
ventana_dorm_sec = A.crear_ventana("VentanaDormSec", ancho=1.8, alto=1.2, origen=(0.8, fondo_total, 1.2))