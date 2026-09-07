import blender_arch as A
import bpy

bpy.ops.wm.read_homefile(use_empty=True)

A.crear_terreno_plano('Terreno_Cesped', ancho=20.0, fondo=30.0, espesor=0.3, material='Cesped')