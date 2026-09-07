import blender_arch as A
import bpy
bpy.ops.wm.read_homefile(use_empty=True)
A.crear_terreno_plano(nombre="Cesped_Jardin", ancho=15.0, fondo=10.0, espesor=0.2, material="Cesped")