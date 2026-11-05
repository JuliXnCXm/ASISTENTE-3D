import blender_arch as A
import bpy
import math

A.limpiar_escena()

ANCHO_TERRAZA = 12.0
FONDO_TERRAZA = 8.0

# --- 1. Base de la azotea y pretil ---
A.crear_losa_rectangular("LosaAzotea", ancho=ANCHO_TERRAZA, fondo=FONDO_TERRAZA, espesor=0.3, origen=(0,0,-0.15))
A.crear_muro("Pretil.Frente", largo=ANCHO_TERRAZA, alto=1.0, origen=(-ANCHO_TERRAZA/2, FONDO_TERRAZA/2, 0), material="Hormigon")
A.crear_muro("Pretil.Fondo", largo=ANCHO_TERRAZA, alto=1.0, origen=(-ANCHO_TERRAZA/2, -FONDO_TERRAZA/2, 0), material="Hormigon")
A.crear_muro("Pretil.Derecha", largo=FONDO_TERRAZA, alto=1.0, origen=(ANCHO_TERRAZA/2, -FONDO_TERRAZA/2, 0), material="Hormigon")

# --- 2. Deck de madera ---
A.crear_piso("DeckMadera", ancho=ANCHO_TERRAZA - 1.2, fondo=FONDO_TERRAZA - 1.2, espesor=0.05, material="Madera_Roble")

# --- 3. Jardineras perimetrales ---
def crear_jardinera(nombre, origen, ancho, fondo):
    bpy.ops.mesh.primitive_cube_add(location=(origen[0], origen[1], 0.3))
    jardinera = bpy.context.active_object
    jardinera.name = nombre
    jardinera.scale = (ancho, fondo, 0.6)
    A.asignar_material(jardinera, nombre="Hormigon", base_color=(0.6,0.6,0.6,1))
    
    # Tierra
    bpy.ops.mesh.primitive_cube_add(location=(origen[0], origen[1], 0.5))
    tierra = bpy.context.active_object
    tierra.name = f"{nombre}.Tierra"
    tierra.scale = (ancho - 0.2, fondo - 0.2, 0.2)
    A.asignar_material(tierra, nombre="Terreno", base_color=(0.2, 0.1, 0.05, 1))

    # Vegetación simple
    for i in range(int(ancho)):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.2, location=(origen[0] - ancho/2 + 0.5 + i, origen[1], 0.7))
        bpy.context.active_object.scale.z = 1.5
        A.asignar_material(bpy.context.active_object, "Vegetacion", base_color=(0.1, 0.5, 0.1, 1))

crear_jardinera("Jardinera.Larga", origen=(0, FONDO_TERRAZA/2 - 0.3, 0), ancho=ANCHO_TERRAZA - 1.2, fondo=0.6)
crear_jardinera("Jardinera.Corta1", origen=(-ANCHO_TERRAZA/2 + 0.3, 0, 0), ancho=0.6, fondo=FONDO_TERRAZA - 1.2)
crear_jardinera("Jardinera.Corta2", origen=(ANCHO_TERRAZA/2 - 0.3, 0, 0), ancho=0.6, fondo=FONDO_TERRAZA - 1.2)

# --- 4. Pérgola de acero ---
MATERIAL_PERGOLA = "Acero"
ORIGEN_PERGOLA = (2.5, -1.5, 0)
ALTO_PERGOLA = 2.8
ANCHO_PERGOLA = 4.0
FONDO_PERGOLA = 3.0

# Postes
A.crear_columna("Poste1", seccion="rect", ancho=0.1, fondo=0.1, alto=ALTO_PERGOLA, origen=(ORIGEN_PERGOLA[0], ORIGEN_PERGOLA[1], 0), material=MATERIAL_PERGOLA)
A.crear_columna("Poste2", seccion="rect", ancho=0.1, fondo=0.1, alto=ALTO_PERGOLA, origen=(ORIGEN_PERGOLA[0] + ANCHO_PERGOLA, ORIGEN_PERGOLA[1], 0), material=MATERIAL_PERGOLA)
A.crear_columna("Poste3", seccion="rect", ancho=0.1, fondo=0.1, alto=ALTO_PERGOLA, origen=(ORIGEN_PERGOLA[0], ORIGEN_PERGOLA[1] + FONDO_PERGOLA, 0), material=MATERIAL_PERGOLA)
A.crear_columna("Poste4", seccion="rect", ancho=0.1, fondo=0.1, alto=ALTO_PERGOLA, origen=(ORIGEN_PERGOLA[0] + ANCHO_PERGOLA, ORIGEN_PERGOLA[1] + FONDO_PERGOLA, 0), material=MATERIAL_PERGOLA)

# Vigas principales
bpy.ops.mesh.primitive_cube_add(location=(ORIGEN_PERGOLA[0] + ANCHO_PERGOLA/2, ORIGEN_PERGOLA[1], ALTO_PERGOLA + 0.05))
viga1 = bpy.context.active_object
viga1.scale = (ANCHO_PERGOLA + 0.1, 0.05, 0.1)
viga1.name = "Viga1"
bpy.ops.mesh.primitive_cube_add(location=(ORIGEN_PERGOLA[0] + ANCHO_PERGOLA/2, ORIGEN_PERGOLA[1] + FONDO_PERGOLA, ALTO_PERGOLA + 0.05))
viga2 = bpy.context.active_object
viga2.scale = (ANCHO_PERGOLA + 0.1, 0.05, 0.1)
viga2.name = "Viga2"

# Travesaños
for i in range(7):
    x_pos = ORIGEN_PERGOLA[0] + (i * ANCHO_PERGOLA / 6)
    bpy.ops.mesh.primitive_cube_add(location=(x_pos, ORIGEN_PERGOLA[1] + FONDO_PERGOLA/2, ALTO_PERGOLA + 0.15))
    trav = bpy.context.active_object
    trav.scale = (0.04, FONDO_PERGOLA, 0.04)
    trav.name = f"Travesano.{i}"

# --- 5. Mobiliario y entorno ---
A.crear_sofa("SofaTerraza", ancho=2.5, origen=(ORIGEN_PERGOLA[0] + 1.2, ORIGEN_PERGOLA[1] + 1, 0), material="Tela_Gris")

# --- 6. Iluminación y cámara ---
A.agregar_luz("Sol", tipo="SUN", ubicacion=(8, -10, 12), energia=6)
Sol = bpy.data.objects['Sol']
Sol.rotation_euler = (math.radians(45), math.radians(-10), math.radians(40))
A.crear_camara("CamaraTerraza", ubicacion=(-8, -10, 7), rotacion=(math.radians(70), 0, math.radians(-40)), activa=True)