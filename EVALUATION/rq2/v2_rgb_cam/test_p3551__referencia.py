import blender_arch as A
import bpy
import math

A.limpiar_escena()

# --- Base de la Azotea ---
ancho_t, fondo_t = 12, 10
techo = A.crear_techo_plano("BaseAzotea", ancho=ancho_t, fondo=fondo_t, espesor=0.3, origen=(0,0,0), material="Hormigon")
deck = A.crear_piso("DeckMadera", ancho=ancho_t, fondo=fondo_t, espesor=0.05, origen=(0,0,0.3), material="Madera_Roble")

# --- Jardineras Perimetrales ---
altura_jardinera = 0.7
grosor_jardinera = 0.2
jardinera_perimetral = A.extruir_con_huecos(
    nombre="MuroJardinera",
    contorno=[(-ancho_t/2, -fondo_t/2), (ancho_t/2, -fondo_t/2), (ancho_t/2, fondo_t/2), (-ancho_t/2, fondo_t/2)],
    agujeros=[[(-ancho_t/2 + grosor_jardinera, -fondo_t/2 + grosor_jardinera), 
               (ancho_t/2 - grosor_jardinera, -fondo_t/2 + grosor_jardinera), 
               (ancho_t/2 - grosor_jardinera, fondo_t/2 - grosor_jardinera), 
               (-ancho_t/2 + grosor_jardinera, fondo_t/2 - grosor_jardinera)]],
    altura=altura_jardinera,
    material="Estuco"
)
jardinera_perimetral.location.z = 0.3

tierra_jardinera = A.crear_piso(
    "TierraJardinera", 
    ancho=ancho_t - 2 * grosor_jardinera, 
    fondo=fondo_t - 2 * grosor_jardinera, 
    espesor=altura_jardinera - 0.1,
    origen=(0, 0, 0.35),
    material="Terreno"
)

# --- Plantas ---
def plantar_arbusto(nombre, origen):
    A.crear_arbol_simple(
        nombre=nombre,
        radio_copa=0.4, altura_copa=0.5, altura_tronco=0.1,
        origen=origen
    )
count = 0
for i in range(int(-ancho_t/2 + 1), int(ancho_t/2), 2):
    plantar_arbusto(f"Arbusto_{count}", origen=(i, fondo_t/2 - 0.5, 0.3 + altura_jardinera))
    count += 1
    plantar_arbusto(f"Arbusto_{count}", origen=(i, -fondo_t/2 + 0.5, 0.3 + altura_jardinera))
    count += 1

# --- Pérgola de Metal ---
origen_pergola = (-4, -3, 0.35)
alto_pergola = 2.5
dim_poste = 0.1
A.crear_columna("Poste1", seccion="rect", ancho=dim_poste, fondo=dim_poste, alto=alto_pergola, origen=origen_pergola, material="Acero")
A.crear_columna("Poste2", seccion="rect", ancho=dim_poste, fondo=dim_poste, alto=alto_pergola, origen=(origen_pergola[0]+4, origen_pergola[1], origen_pergola[2]), material="Acero")
A.crear_columna("Poste3", seccion="rect", ancho=dim_poste, fondo=dim_poste, alto=alto_pergola, origen=(origen_pergola[0]+4, origen_pergola[1]+4, origen_pergola[2]), material="Acero")
A.crear_columna("Poste4", seccion="rect", ancho=dim_poste, fondo=dim_poste, alto=alto_pergola, origen=(origen_pergola[0], origen_pergola[1]+4, origen_pergola[2]), material="Acero")

def crear_viga_pergola(nombre, origen, largo, rot_z=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=origen)
    viga = bpy.context.active_object
    viga.name = nombre
    viga.scale = (largo, 0.1, 0.15)
    viga.rotation_euler[2] = math.radians(rot_z)
    A.asignar_material(viga, "Acero")
    return viga

crear_viga_pergola("Viga1", origen=(origen_pergola[0]+2, origen_pergola[1], origen_pergola[2]+alto_pergola), largo=4.1)
crear_viga_pergola("Viga2", origen=(origen_pergola[0]+2, origen_pergola[1]+4, origen_pergola[2]+alto_pergola), largo=4.1)
crear_viga_pergola("Viga3", origen=(origen_pergola[0], origen_pergola[1]+2, origen_pergola[2]+alto_pergola), largo=4.1, rot_z=90)
crear_viga_pergola("Viga4", origen=(origen_pergola[0]+4, origen_pergola[1]+2, origen_pergola[2]+alto_pergola), largo=4.1, rot_z=90)

# --- Mobiliario ---
sofa = A.crear_sofa("SofaExterior", ancho=2.5, fondo=0.8, alto_asiento=0.4, origen=(-2, -1, 0.35), material="Tela_Beige")
mesa = A.crear_mesa("MesaBaja", ancho=1.2, fondo=0.7, alto=0.4, origen=(-2, 1.5, 0.35), material_tablero="Madera", material_patas="Acero")

# --- Iluminación y Cámara ---
A.agregar_luz("LuzSol", tipo="SUN", ubicacion=(8, -10, 15), energia=4)
A.crear_camara("CamaraTerraza", ubicacion=(10, -9, 6), rotacion=(70, 0, 45))