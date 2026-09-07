import blender_arch as A
import bpy

A.limpiar_escena()

# Base de la azotea
ancho_terraza = 10
fondo_terraza = 8
losa_azotea = A.crear_losa_rectangular("LosaAzotea", ancho=ancho_terraza, fondo=fondo_terraza, espesor=0.3, origen=(0, 0, -0.15))
A.asignar_material(losa_azotea, nombre="Hormigon")

# Deck de madera con bpy
plank_w, plank_l, plank_t = 0.14, fondo_terraza, 0.025
bpy.ops.mesh.primitive_cube_add(size=1, location=(-ancho_terraza/2 + plank_w/2, 0, plank_t/2))
plank = bpy.context.active_object
plank.name = "PlankMaestro"
plank.scale = (plank_w, plank_l, plank_t)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
A.asignar_material(plank, nombre="Madera_Roble")

mod_array = plank.modifiers.new(name="ArrayDeck", type='ARRAY')
mod_array.relative_offset_displace[0] = 1.05
mod_array.count = int(ancho_terraza / (plank_w * 1.05))

# Jardineras perimetrales
def crear_jardinera(nombre, largo, ancho, origen, rot_z=0):
    jardinera = A.extruir_con_huecos(nombre,
        contorno=[(-largo/2, -ancho/2), (largo/2, -ancho/2), (largo/2, ancho/2), (-largo/2, ancho/2)],
        agujeros=[[(-largo/2+0.1, -ancho/2+0.1), (largo/2-0.1, -ancho/2+0.1), (largo/2-0.1, ancho/2-0.1), (-largo/2+0.1, ancho/2-0.1)]],
        altura=0.6,
        material="Hormigon"
    )
    jardinera.location = origen
    jardinera.rotation_euler.z = rot_z
    tierra = A.crear_piso(f"Tierra_{nombre}", ancho=largo-0.2, fondo=ancho-0.2, espesor=0.02, origen=(origen[0], origen[1], 0.55))
    tierra.rotation_euler.z = rot_z
    A.asignar_material(tierra, nombre="Terreno")
    A.crear_arbol_simple(f"Planta_{nombre}", radio_copa=0.5, altura_copa=0.6, altura_tronco=0.1, origen=(origen[0], origen[1], 0.6))

crear_jardinera("JardineraFondo", largo=ancho_terraza, ancho=0.5, origen=(0, fondo_terraza/2 - 0.25, 0))
crear_jardinera("JardineraDerecha", largo=fondo_terraza-0.5, ancho=0.5, origen=(ancho_terraza/2 - 0.25, -0.25, 0), rot_z=1.5708)
crear_jardinera("JardineraIzquierda", largo=fondo_terraza-0.5, ancho=0.5, origen=(-ancho_terraza/2 + 0.25, -0.25, 0), rot_z=1.5708)

# Pérgola metálica
pergola_origen = (0, -1.5, 0)
pergola_ancho = 4
pergola_fondo = 4
pergola_alto = 2.8

for i in [-1, 1]:
    for j in [-1, 1]:
        x = pergola_origen[0] + i * pergola_ancho / 2
        y = pergola_origen[1] + j * pergola_fondo / 2
        A.crear_columna(f"PostePergola_{i}_{j}", seccion="rect", ancho=0.1, fondo=0.1, alto=pergola_alto, origen=(x, y, 0), material="Marco_Negro")

viga_perim_1 = A.extruir_perfil("VigaPerim1", [(-0.05, -0.1), (0.05, -0.1), (0.05, 0.1), (-0.05, 0.1)], altura=pergola_ancho, material="Marco_Negro")
viga_perim_1.location = (pergola_origen[0], pergola_origen[1] - pergola_fondo/2, pergola_alto)
viga_perim_1.rotation_euler.y = 1.5708

viga_perim_2 = A.extruir_perfil("VigaPerim2", [(-0.05, -0.1), (0.05, -0.1), (0.05, 0.1), (-0.05, 0.1)], altura=pergola_ancho, material="Marco_Negro")
viga_perim_2.location = (pergola_origen[0], pergola_origen[1] + pergola_fondo/2, pergola_alto)
viga_perim_2.rotation_euler.y = 1.5708

# Mobiliario y entorno
sofa = A.crear_sofa("SofaExterior", ancho=2.5, fondo=0.9, origen=(pergola_origen[0], pergola_origen[1], 0), material="Tela_Gris")

# Iluminación y cámara
A.agregar_luz("LuzTerraza", tipo="SUN", ubicacion=(-10, -8, 12), energia=3.5)
A.crear_camara("CamaraTerraza", ubicacion=(8, -10, 5), rotacion=(70, 0, 40), activa=True)