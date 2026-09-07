import blender_arch as A
import bpy
bpy.ops.wm.read_homefile(use_empty=True)
A.crear_arbol_simple(nombre='ArbolGrande', radio_copa=2.0, altura_copa=4.0, altura_tronco=2.5)