import blender_arch as A
import bpy
import math

A.limpiar_escena()

# 1. Crear la base de la plaza
plaza_suelo = A.crear_terreno_plano("PlazaSuelo", ancho=30, fondo=20, espesor=0.2, origen=(0, 0, -0.1))
A.asignar_material(plaza_suelo, nombre="AdoquinHormigon", base_color=(0.4, 0.4, 0.4, 1.0))

# 2. Crear alcorque elevado y árbol
alcorque_borde = A.extruir_con_huecos(
    nombre="AlcorqueBorde", 
    contorno=[(-1.5, -1.5), (1.5, -1.5), (1.5, 1.5), (-1.5, 1.5)], 
    agujeros=[[(-1.2, -1.2), (1.2, -1.2), (1.2, 1.2), (-1.2, 1.2)]], 
    altura=0.4, 
    material="Hormigon"
)
alcorque_borde.location = (0, 0, 0)

alcorque_tierra = A.crear_piso("AlcorqueTierra", ancho=2.4, fondo=2.4, espesor=0.38, origen=(0, 0, 0.01), material="Terreno")
arbol = A.crear_arbol_simple("ArbolCentral", radio_copa=3.5, altura_copa=5.0, altura_tronco=2.5, origen=(0, 0, 0.4))

# 3. Diseñar y colocar bancas personalizadas
def crear_banca_moderna(nombre, origen):
    # Asiento de hormigón
    bpy.ops.mesh.primitive_cube_add(size=1, location=(origen[0], origen[1], origen[2] + 0.2))
    asiento = bpy.context.active_object
    asiento.name = f"{nombre}_Asiento"
    asiento.scale = (2.0, 0.5, 0.1)
    A.asignar_material(asiento, "Hormigon")
    
    # Respaldo de madera
    bpy.ops.mesh.primitive_cube_add(size=1, location=(origen[0], origen[1] + 0.2, origen[2] + 0.5))
    respaldo = bpy.context.active_object
    respaldo.name = f"{nombre}_Respaldo"
    respaldo.scale = (2.0, 0.05, 0.4)
    A.asignar_material(respaldo, "Madera_Roble")
    
    # Unir partes (opcional, para organización)
    bpy.ops.object.select_all(action='DESELECT')
    asiento.select_set(True)
    respaldo.select_set(True)
    bpy.context.view_layer.objects.active = asiento
    bpy.ops.object.parent_set(type='OBJECT')

crear_banca_moderna("Banca.001", origen=(8, 5, 0))
crear_banca_moderna("Banca.002", origen=(8, -5, 0))
crear_banca_moderna("Banca.003", origen=(-8, 5, 0))
crear_banca_moderna("Banca.004", origen=(-8, -5, 0))

# 4. Diseñar y colocar farolas
def crear_farola(nombre, origen):
    # Poste
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=6, location=(origen[0], origen[1], origen[2] + 3))
    poste = bpy.context.active_object
    poste.name = f"{nombre}_Poste"
    A.asignar_material(poste, "Acero_Inox")

    # Brazo
    bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=1.5, location=(origen[0], origen[1] + 0.75, origen[2] + 5.8))
    brazo = bpy.context.active_object
    brazo.name = f"{nombre}_Brazo"
    brazo.rotation_euler[0] = math.radians(90)
    A.asignar_material(brazo, "Acero_Inox")
    
    # Luminaria y luz
    bpy.ops.mesh.primitive_cube_add(size=1, location=(origen[0], origen[1] + 1.4, origen[2] + 5.8))
    luminaria = bpy.context.active_object
    luminaria.name = f"{nombre}_Luminaria"
    luminaria.scale = (0.3, 0.4, 0.1)
    A.asignar_material(luminaria, "Marco_Negro")
    A.agregar_luz(f"Luz_{nombre}", tipo="SPOT", ubicacion=(origen[0], origen[1] + 1.4, origen[2] + 5.7), energia=1500, color=(1, 0.9, 0.7))

crear_farola("Farola.001", origen=(12, 8, 0))
crear_farola("Farola.002", origen=(12, -8, 0))
crear_farola("Farola.003", origen=(-12, 8, 0))
crear_farola("Farola.004", origen=(-12, -8, 0))

# 5. Iluminación general y cámara
A.agregar_luz("LuzSol", tipo="SUN", ubicacion=(5, -10, 15), energia=5)
A.crear_camara("CamaraPlaza", ubicacion=(18, -15, 10), rotacion=(70, 0, 40))