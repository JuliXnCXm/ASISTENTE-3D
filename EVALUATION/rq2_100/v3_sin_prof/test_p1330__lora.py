import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

A.crear_terreno_plano(nombre="Parcela", ancho=20, fondo=16, espesor=0.2, material="Cesped")
A.crear_casa_n_pisos(
    nombre="Casa_Familiar",
    pisos=2,
    ancho=10.0,
    fondo=8.0,
    alto_piso=2.8,
    origen=(0, 0, 0.1),
    material_muro="Ladrillo_Rojo",
    material_losa="Hormigon",
    material_tejado="Teja"
)
A.crear_arbol_simple(nombre="Arbol_1", origen=(-4, -3, 0.1))
A.crear_arbol_simple(nombre="Arbol_2", radio_copa=1.5, altura_copa=3.0, origen=(4, 2, 0.1))