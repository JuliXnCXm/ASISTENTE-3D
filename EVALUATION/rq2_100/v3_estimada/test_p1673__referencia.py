import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Parcela de terreno
A.crear_terreno_plano(
    nombre="Jardin_Casa", 
    ancho=30, 
    fondo=25, 
    espesor=0.3, 
    origen=(0, 0, -0.15), 
    material="Cesped"
)

# Casa de dos pisos
A.crear_casa_n_pisos(
    nombre="Casa_Familiar", 
    pisos=2, 
    ancho=12, 
    fondo=9, 
    alto_piso=2.8, 
    con_tejado=True, 
    altura_cumbrera=1.8, 
    voladizo=0.5, 
    material_muro="Ladrillo", 
    material_losa="Hormigon", 
    material_tejado="Teja"
)

# Colocar árboles
A.crear_arbol_simple("Arbol_1", radio_copa=2, altura_copa=4, altura_tronco=2, origen=(-10, 8, 0))
A.crear_arbol_simple("Arbol_2", radio_copa=1.5, altura_copa=3, altura_tronco=1.5, origen=(10, -10, 0))
A.crear_arbol_simple("Arbol_3", radio_copa=1.8, altura_copa=3.5, altura_tronco=1.8, origen=(8, 9, 0))