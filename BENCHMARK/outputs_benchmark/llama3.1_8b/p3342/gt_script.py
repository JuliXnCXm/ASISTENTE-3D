import blender_arch as A
import bpy

A.limpiar_escena()

# --- Dimensiones --- #
# Ala de día (horizontal)
ANCHO_DIA = 12.0
FONDO_DIA = 5.0
# Ala de noche (vertical)
ANCHO_NOCHE = 5.0
FONDO_NOCHE = 11.0
# Generales
ALTO_MURO = 3.0
GROSOR_MURO = 0.2
GROSOR_LOSA = 0.2

# --- Orígenes de las alas --- #
origen_dia = (0, FONDO_NOCHE - FONDO_DIA, 0)
origen_noche = (0, 0, 0)

# --- Materiales --- #
mat_muro_ext = "Estuco"
mat_muro_int = "Muro_Pintura"
mat_piso_int = "Porcelanato"
mat_piso_patio = "Ceramica_Piso"

# --- Suelos --- #
piso_dia = A.crear_piso("PisoDia", ANCHO_DIA, FONDO_DIA, 0.02, origen_dia, material=mat_piso_int)
piso_noche = A.crear_piso("PisoNoche", ANCHO_NOCHE, FONDO_NOCHE, 0.02, origen_noche, material=mat_piso_int)
piso_patio = A.crear_piso("PisoPatio", ANCHO_DIA-ANCHO_NOCHE, FONDO_NOCHE-FONDO_DIA, 0.02, origen=(ANCHO_NOCHE, 0, 0), material=mat_piso_patio)

# --- Muros Perimetrales --- #
muros = []
# Ala Día
muros.append(A.crear_muro("MuroDiaFondo", ANCHO_DIA, ALTO_MURO, GROSOR_MURO, origen=(0, FONDO_NOCHE, 0)))
muros.append(A.crear_muro("MuroDiaDer", FONDO_DIA, ALTO_MURO, GROSOR_MURO, origen=(ANCHO_DIA, FONDO_NOCHE - FONDO_DIA, 0), rotacion_z=90))
# Ala Noche
muros.append(A.crear_muro("MuroNocheFrente", ANCHO_NOCHE, ALTO_MURO, GROSOR_MURO, origen=(0, 0, 0)))
muros.append(A.crear_muro("MuroNocheIzq", FONDO_NOCHE, ALTO_MURO, GROSOR_MURO, origen=(0, 0, 0), rotacion_z=90))
# Muros hacia el patio (interiores de la L)
muros.append(A.crear_muro("MuroPatio1", ANCHO_DIA-ANCHO_NOCHE, ALTO_MURO, GROSOR_MURO, origen=(ANCHO_NOCHE, FONDO_NOCHE - FONDO_DIA, 0)))
muros.append(A.crear_muro("MuroPatio2", FONDO_NOCHE-FONDO_DIA, ALTO_MURO, GROSOR_MURO, origen=(ANCHO_NOCHE, 0, 0), rotacion_z=90))

for m in muros: A.asignar_material(m, nombre=mat_muro_ext)

# --- Muros Interiores (Ala Noche) --- #
# Dormitorio principal en suite
muros.append(A.crear_muro("DivDormPpal", ANCHO_NOCHE, ALTO_MURO, GROSOR_MURO, origen=(0, 4.0, 0)))
muros.append(A.crear_muro("DivBanoSuite", 1.8, ALTO_MURO, GROSOR_MURO, origen=(ANCHO_NOCHE - 1.8, 0, 0), rotacion_z=90))
# Dormitorios secundarios y baño común
muros.append(A.crear_muro("DivDorm2", ANCHO_NOCHE, ALTO_MURO, GROSOR_MURO, origen=(0, 7.5, 0)))
muros.append(A.crear_muro("DivBanoComun", 2.5, ALTO_MURO, GROSOR_MURO, origen=(0, 4.0, 0), rotacion_z=90))

# --- Mobiliario --- #
# Zona Día
sofa_l = A.crear_sofa("Sofa", ancho=3.0, origen=(ANCHO_NOCHE + 0.5, FONDO_NOCHE - FONDO_DIA + 0.5, 0), material="Tela_Beige")
mesa_comedor = A.crear_mesa("MesaComedor", ancho=2.2, fondo=1.0, origen=(ANCHO_DIA - 2.7, FONDO_NOCHE-FONDO_DIA+2.0, 0))
isla_cocina = A.crear_mesa("IslaCocina", ancho=2.5, fondo=1.2, alto=0.9, origen=(1.5, FONDO_NOCHE - 2.0, 0), material_tablero="Porcelanato")

# Zona Noche
# Dorm Ppal
cama_ppal = A.crear_cama("CamaPpal", ancho=1.8, largo=2.0, origen=(1.0, 0.5, 0))
armario_ppal = A.crear_armario("ArmarioPpal", ancho=2.5, alto=ALTO_MURO, fondo=0.6, origen=(ANCHO_NOCHE-2.7, 3.2, 0))
# Dorm 2
cama2 = A.crear_cama("Cama2", ancho=1.0, largo=2.0, origen=(ANCHO_NOCHE - 1.5, 4.5, 0))
# Dorm 3
cama3 = A.crear_cama("Cama3", ancho=1.0, largo=2.0, origen=(ANCHO_NOCHE - 1.5, 8.0, 0))

# --- Techos --- #
techo_dia = A.crear_techo_plano("TechoDia", ANCHO_DIA, FONDO_DIA, GROSOR_LOSA, origen=origen_dia, caida_x=0.01)
techo_dia.location.z = ALTO_MURO
techo_noche = A.crear_techo_plano("TechoNoche", ANCHO_NOCHE, FONDO_NOCHE, GROSOR_LOSA, origen=origen_noche, caida_y=0.01)
techo_noche.location.z = ALTO_MURO

# --- Exterior y Vistas --- #
arbol_patio = A.crear_arbol_simple("ArbolPatio", radio_copa=2.0, altura_copa=3.5, altura_tronco=2.0, origen=(ANCHO_NOCHE + 2, 2, 0))

# Vano grande hacia el patio
vano_patio = A.abrir_vanos_batch_rectangulares(muros[4], centros_world=[(ANCHO_NOCHE + (ANCHO_DIA-ANCHO_NOCHE)/2, FONDO_NOCHE-FONDO_DIA, 1.5)], ancho=5, alto=2.5)

# --- Iluminación y Cámara --- #
A.agregar_luz("LuzSolar", tipo="SUN", ubicacion=(-15, 15, 20), energia=3.0)
A.crear_camara("CamaraVistaAerea", ubicacion=(ANCHO_DIA+5, -5, 12), rotacion=(65, 0, 135))