import blender_arch as A
import bpy
bpy.ops.wm.read_homefile(use_empty=True)
A.crear_casa_n_pisos(nombre='CasaFamiliar', pisos=2, ancho=12.0, fondo=8.0, alto_piso=3.0, grosor_muro=0.25, voladizo=0.5, material_muro='Ladrillo_Rojo', material_losa='Hormigon', material_tejado='Teja')
A.crear_tejado_dos_aguas(nombre='TechoCasa', ancho=12.0, fondo=8.0, altura_cumbrera=3.0, espesor=0.15, voladizo_x=0.5, voladizo_y=0.5, origen=(0, 0, 6.0), material='Teja')