import blender_arch as A
import bpy
bpy.ops.wm.read_homefile(use_empty=True)
A.crear_terreno_plano('Jardin_Casa', ancho=30.0, fondo=25.0, espesor=0.3, material='Cesped')
A.crear_casa_n_pisos('Casa_Familiar', pisos=2, ancho=10.0, fondo=8.0, alto_piso=2.8, con_tejado=True, origen=(0, 0, 0.15), material_muro='Estuco', material_tejado='Teja')
A.crear_arbol_simple('Arbol_Jardin', radio_copa=2.0, altura_copa=4.0, altura_tronco=2.0, origen=(-10, 8, 0.15))