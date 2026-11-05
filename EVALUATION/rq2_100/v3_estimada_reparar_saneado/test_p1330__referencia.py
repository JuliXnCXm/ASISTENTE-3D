import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

A.crear_terreno_plano(
    nombre="Jardin",
    ancho=25.0,
    fondo=30.0,
    espesor=0.2,
    origen=(-7.5, -15, -0.2),
    material="Cesped"
)

A.crear_casa_n_pisos(
    nombre="Casa_Familiar",
    pisos=2,
    ancho=10.0,
    fondo=8.0,
    alto_piso=2.8,
    con_tejado=True,
    altura_cumbrera=2.0,
    voladizo=0.5,
    material_muro="Ladrillo",
    material_tejado="Teja_Zinc"
)

A.crear_arbol_simple(
    nombre="Arbol_Izquierdo",
    radio_copa=1.8,
    altura_copa=3.2,
    altura_tronco=2.0,
    origen=(-3, -5, 0)
)

A.crear_arbol_simple(
    nombre="Arbol_Derecho",
    radio_copa=1.5,
    altura_copa=2.8,
    altura_tronco=1.8,
    origen=(13, -6, 0)
)