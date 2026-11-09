import blender_arch as A
import bpy
bpy.ops.wm.read_homefile(use_empty=True)
A.crear_casa_n_pisos(nombre='Casa_Familiar', pisos=2, ancho=12.0, fondo=10.0, alto_piso=3.0, grosor_muro=0.25, altura_cumbrera=2.5, voladizo=0.5, origen=(0, 0, 0), material_muro='Ladrillo_Rojo', material_losa='Hormigon', material_tejado='Teja')