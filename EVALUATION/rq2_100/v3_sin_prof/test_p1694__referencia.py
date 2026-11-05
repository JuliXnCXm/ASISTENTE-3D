import blender_arch as A
import bpy
bpy.ops.wm.read_homefile(use_empty=True)

# Crear el terreno
A.crear_terreno_plano(
    nombre="Parcela_Casa",
    ancho=25.0,
    fondo=20.0,
    espesor=0.5,
    origen=(0, 0, -0.25),
    material="Cesped"
)

# Crear la casa
A.crear_casa_n_pisos(
    nombre="Casa_Familiar",
    pisos=2,
    ancho=12.0,
    fondo=9.0,
    alto_piso=2.8,
    grosor_muro=0.25,
    con_tejado=True,
    altura_cumbrera=2.0,
    voladizo=0.5,
    origen=(-6, -4.5, 0),
    material_muro="Ladrillo_Rojo",
    material_losa="Hormigon",
    material_tejado="Teja"
)

# Añadir árboles
A.crear_arbol_simple(
    nombre="Arbol_1",
    radio_copa=1.8,
    altura_copa=3.0,
    altura_tronco=1.8,
    origen=(8, 6, 0)
)
A.crear_arbol_simple(
    nombre="Arbol_2",
    radio_copa=2.2,
    altura_copa=4.0,
    altura_tronco=2.0,
    origen=(-9, -7, 0)
)

# Añadir cámara para una buena vista
A.crear_camara(
    nombre="Camara_Exterior",
    ubicacion=(15, -18, 8),
    rotacion=(70, 0, 30)
)