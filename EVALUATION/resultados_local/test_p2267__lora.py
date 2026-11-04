import blender_arch as A
import bpy

A.limpiar_escena()

# 1. Base de la plaza
plaza = A.crear_terreno_plano("Plaza", ancho=20, fondo=20, espesor=0.2, origen=(0,0,-0.1), material="Concreto_Piso")

# 2. Fuente central de múltiples niveles
for i in range(4):
    altura = i * 0.5 + 0.5
    radio = i * 1.5 + 1.5
    nombre = f"Fuente_Nivel_{i+1}"
    A.extruir_con_huecos(f"Base_Fuente_{nombre}", 
                         contorno=[(-radio/2, -radio/2), (radio/2, -radio/2), (radio/2, radio/2), (-radio/2, radio/2)], 
                         agujeros=[[(-radio*0.8, -radio*0.8), (radio*0.8, -radio*0.8), (radio*0.8, radio*0.8), (-radio*0.8, radio*0.8)]], 
                         altura=altura, material="Acero_Inox")
    A.asignar_material(A.get_objects(nombre)[0], nombre="Acero_Inox")

# 3. Bancos de hormigón a medida
for i in range(3):
    A.crear_silla(f"Banco_{i+1}", ancho=2.0, fondo=0.5, alto_asiento=0.45, alto_respaldo=0.1, origen=(-7 + i*3, 9, 0), material="Hormigon")

# 4. Pérgola de madera con patrón de vigas
origen_pergola = (0, -8, 0)
A.crear_columna("Poste_1", seccion="rect", ancho=0.2, fondo=0.2, alto=2.5, origen=(origen_pergola[0], origen_pergola[1], origen_pergola[2]), material="Madera_Roble")
A.crear_columna("Poste_2", seccion="rect", ancho=0.2, fondo=0.2, alto=2.5, origen=(origen_pergola[0]+3, origen_pergola[1], origen_pergola[2]), material="Madera_Roble")
A.crear_columna("Poste_3", seccion="rect", ancho=0.2, fondo=0.2, alto=2.5, origen=(origen_pergola[0]+6, origen_pergola[1], origen_pergola[2]), material="Madera_Roble")
A.crear_columna("Poste_4", seccion="rect", ancho=0.2, fondo=0.2, alto=2.5, origen=(origen_pergola[0], origen_pergola[1]-3, origen_pergola[2]), material="Madera_Roble")
A.crear_columna("Poste_5", seccion="rect", ancho=0.2, fondo=0.2, alto=2.5, origen=(origen_pergola[0]+3, origen_pergola[1]-3, origen_pergola[2]), material="Madera_Roble")
A.crear_columna("Poste_6", seccion="rect", ancho=0.2, fondo=0.2, alto=2.5, origen=(origen_pergola[0]+6, origen_pergola[1]-3, origen_pergola[2]), material="Madera_Roble")

viga_principal = A.extruir_perfil("Viga_Principal", puntos_2d=[(0,0), (4,0), (4,0.2), (0,0.2)], altura=2.5, material="Madera_Roble")
viga_principal.location = (origen_pergola[0]+3, origen_pergola[1]-1.5, origen_pergola[2]+0.1)

# Vigas secundarias con patrón
for i in range(5):
    x_pos = origen_pergola[0] + 3 + i * 0.8
    viga_sec = A.extruir_perfil(f"Viga_Secundaria_{i}", puntos_2d=[(0,0), (2,0), (2,0.15), (0,0.15)], altura=2.5, material="Madera_Roble")
    viga_sec.location = (x_pos, origen_pergola[1]-1.5, origen_pergola[2]+0.6)
    A.asignar_material(viga_sec, nombre="Madera_Roble")