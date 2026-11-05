import blender_arch as A
import bpy

def crear_modulo_cocina(nombre, origen, ancho=0.6, fondo=0.6, alto=0.9, material="MDF_Blanco"):
    bpy.ops.mesh.primitive_cube_add(size=1, location=origen)
    obj = bpy.context.active_object
    obj.name = nombre
    obj.scale = (ancho, fondo, alto)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    A.asignar_material(obj, material)
    return obj

A.limpiar_escena()

# --- Definir Espacio ---
hab = A.crear_habitacion("Cocina", ancho=5, fondo=4.5, alto=2.8, material_muro="Muro_Pintura", material_suelo="Parquet")

# --- Módulos Bajos en L ---
largo_pared1 = 3.5
largo_pared2 = 2.5
grosor_muro = 0.2
prof_modulo = 0.6
alto_modulo_bajo = 0.9

# Pared Larga (Y)
for i in range(int(largo_pared1 / 0.6)):
    x = grosor_muro + 0.6 * i + 0.3
    y = grosor_muro + prof_modulo / 2
    crear_modulo_cocina(f"ModuloBajo_A_{i}", origen=(x, y, alto_modulo_bajo / 2))

# Pared Corta (X)
for i in range(int(largo_pared2 / 0.6)):
    x = grosor_muro + prof_modulo/2
    y = grosor_muro + prof_modulo + (0.6 * i) + 0.3
    crear_modulo_cocina(f"ModuloBajo_B_{i}", origen=(x, y, alto_modulo_bajo / 2))

# --- Encimera en L ---
encimera_l = A.extruir_con_huecos(
    nombre="Encimera",
    contorno=[(grosor_muro, grosor_muro), (largo_pared1, grosor_muro), (largo_pared1, grosor_muro+prof_modulo), (grosor_muro+prof_modulo, grosor_muro+prof_modulo), (grosor_muro+prof_modulo, largo_pared2), (grosor_muro, largo_pared2)],
    agujeros=[],
    altura=0.03,
    material=""
)
encimera_l.location.z = alto_modulo_bajo
A.asignar_material(encimera_l, nombre="CuarzoBlanco", base_color=(0.95, 0.95, 0.98, 1.0))

# --- Módulos Altos ---
alto_modulo_alto = 0.7
prof_modulo_alto = 0.35
z_base_altos = 1.6

for i in range(int(largo_pared1 / 0.6)):
    x = grosor_muro + 0.6 * i + 0.3
    y = grosor_muro + prof_modulo_alto / 2
    crear_modulo_cocina(f"ModuloAlto_{i}", origen=(x, y, z_base_altos + alto_modulo_alto / 2), fondo=prof_modulo_alto, alto=alto_modulo_alto)

# --- Extractor ---
extractor = crear_modulo_cocina("Extractor", origen=(1.5, 0.4, 1.8), ancho=0.8, fondo=0.5, alto=0.5, material="Acero_Inox")

# --- Isla Central ---
isla = crear_modulo_cocina("Isla_Base", origen=(2.5, 2.5, 0.45), ancho=2.0, fondo=1.0, alto=0.9, material="MDF_Blanco")
encimera_isla = crear_modulo_cocina("Isla_Encimera", origen=(2.5, 2.5, 0.915), ancho=2.0, fondo=1.0, alto=0.03)
A.asignar_material(encimera_isla, nombre="CuarzoBlanco", base_color=(0.95, 0.95, 0.98, 1.0))

# --- Taburetes ---
taburete1 = A.crear_silla("Taburete1", ancho=0.4, fondo=0.4, alto_asiento=0.7, alto_respaldo=0.8, origen=(2.0, 3.2, 0), material="Madera_Roble")
taburete2 = A.crear_silla("Taburete2", ancho=0.4, fondo=0.4, alto_asiento=0.7, alto_respaldo=0.8, origen=(2.8, 3.2, 0), material="Madera_Roble")

# --- Iluminación y Cámara ---
A.agregar_luz("LuzPrincipal", tipo="AREA", ubicacion=(2.5, 2.25, 2.6), energia=800)
A.crear_camara("CamaraCocina", ubicacion=(8, -3, 3), rotacion=(75, 0, 120), activa=True)