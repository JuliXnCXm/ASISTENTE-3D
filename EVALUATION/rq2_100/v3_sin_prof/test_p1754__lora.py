import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

A.crear_terreno_plano('Parcela', ancho=20, fondo=15, material='Cesped')
A.crear_casa_n_pisos(
    'Casa_Familiar',
    pisos=2,
    ancho=10.0,
    fondo=8.0,
    alto_piso=2.8,
    origen=(0, 0, 0),
    material_muro='Ladrillo_Rojo',
    material_losa='Hormigon',
    material_tejado='Teja'
)
A.crear_arbol_simple('Arbol_Izq', origen=(-4, -3, 0))
A.crear_arbol_simple('Arbol_Der', origen=(4, 3, 0))