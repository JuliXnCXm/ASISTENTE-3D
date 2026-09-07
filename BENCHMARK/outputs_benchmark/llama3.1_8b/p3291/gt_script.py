import bpy
import blender_arch as A

A.limpiar_escena()

ancho_terraza = 10
fondo_terraza = 15
alto_peto = 1.0

# Base de la azotea (losa y petos/muros perimetrales)
losa_azotea = A.crear_techo_plano(nombre="LosaAzotea", ancho=ancho_terraza, fondo=fondo_terraza, espesor=0.3, origen=(0, 0, -0.15))
A.asignar_material(losa_azotea, "Hormigon")

muro_norte = A.crear_muro(nombre="PetoNorte", largo=ancho_terraza, alto=alto_peto, origen=(-ancho_terraza/2, fondo_terraza/2, 0), material="Hormigon")
muro_sur = A.crear_muro(nombre="PetoSur", largo=ancho_terraza, alto=alto_peto, origen=(-ancho_terraza/2, -fondo_terraza/2, 0), material="Hormigon")
muro_este = A.crear_muro(nombre="PetoEste", largo=fondo_terraza, alto=alto_peto, origen=(ancho_terraza/2, -fondo_terraza/2, 0), material="Hormigon")
muro_oeste = A.crear_muro(nombre="PetoOeste", largo=fondo_terraza, alto=alto_peto, origen=(-ancho_terraza/2, -fondo_terraza/2, 0), material="Hormigon")

# Deck de madera
deck = A.crear_piso(nombre="DeckMadera", ancho=ancho_terraza - 0.2, fondo=fondo_terraza - 0.2, espesor=0.05, origen=(0, 0, 0.025))
A.asignar_material(deck, "Madera_Roble")

# Jardineras perimetrales de hormigón
def crear_jardinera(nombre, largo, ancho, origen):
    bpy.ops.mesh.primitive_cube_add(location=(origen[0], origen[1], origen[2] + 0.4))
    jardinera = bpy.context.active_object
    jardinera.name = nombre
    jardinera.scale = (largo/2, ancho/2, 0.4)
    bpy.ops.object.transform_apply(scale=True, location=False, rotation=False)
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.inset(thickness=0.15, use_boundary=True)
    bpy.ops.transform.translate(value=(0, 0, 10)) # Mover las caras insetadas muy arriba para borrarlas
    bpy.ops.mesh.delete(type='FACE')
    bpy.ops.object.mode_set(mode='OBJECT')

    A.asignar_material(jardinera, "HormigonVisto", base_color=(0.8, 0.8, 0.8, 1))
    
    # Añadir tierra y vegetación simple
    bpy.ops.mesh.primitive_cube_add(location=(origen[0], origen[1], origen[2] + 0.3))
    tierra = bpy.context.active_object
    tierra.name = f"{nombre}_Tierra"
    tierra.scale = ((largo - 0.3)/2, (ancho - 0.3)/2, 0.3)
    A.asignar_material(tierra, "Terreno", base_color=(0.3, 0.2, 0.1, 1))
    
    for i in range(int(largo)):
        x_pos = origen[0] - largo/2 + 0.5 + i
        A.crear_arbol_simple(f"Planta_{nombre}_{i}", radio_copa=0.3, altura_copa=0.5, altura_tronco=0.2, origen=(x_pos, origen[1], 0.8))
    return jardinera

crear_jardinera("JardineraLarga", largo=8, ancho=0.8, origen=(0, 6.7, 0))
crear_jardinera("JardineraCorta1", largo=4, ancho=0.8, origen=(-4.2, -2, 0))
crear_jardinera("JardineraCorta2", largo=4, ancho=0.8, origen=(4.2, -2, 0))


# Pérgola de acero
def crear_pergola(origen, ancho, fondo, alto):
    mat_pergola = "Acero_Inox"
    # Postes
    A.crear_columna("Poste1", seccion="rect", ancho=0.1, fondo=0.1, alto=alto, origen=(origen[0]-ancho/2, origen[1]-fondo/2, 0), material=mat_pergola)
    A.crear_columna("Poste2", seccion="rect", ancho=0.1, fondo=0.1, alto=alto, origen=(origen[0]+ancho/2, origen[1]-fondo/2, 0), material=mat_pergola)
    A.crear_columna("Poste3", seccion="rect", ancho=0.1, fondo=0.1, alto=alto, origen=(origen[0]-ancho/2, origen[1]+fondo/2, 0), material=mat_pergola)
    A.crear_columna("Poste4", seccion="rect", ancho=0.1, fondo=0.1, alto=alto, origen=(origen[0]+ancho/2, origen[1]+fondo/2, 0), material=mat_pergola)
    # Vigas
    A.crear_losa_rectangular("Viga1", ancho+0.1, 0.1, 0.15, origen=(origen[0], origen[1]-fondo/2, alto), material=mat_pergola)
    A.crear_losa_rectangular("Viga2", ancho+0.1, 0.1, 0.15, origen=(origen[0], origen[1]+fondo/2, alto), material=mat_pergola)
    # Listones
    for i in range(int(ancho*4)+1):
        x = origen[0] - ancho/2 + i * 0.25
        A.crear_losa_rectangular(f"Liston.{i}", 0.05, fondo-0.1, 0.1, origen=(x, origen[1], alto+0.125), material=mat_pergola)

crear_pergola(origen=(0, -4, 0), ancho=4, fondo=5, alto=2.8)

# Iluminación y cámara
A.agregar_luz(nombre="Sol", tipo="SUN", ubicacion=(10, 10, 10), energia=8)
A.crear_camara(nombre="CamaraTerraza", ubicacion=(12, -15, 8), rotacion=(70, 0, 30), activa=True)