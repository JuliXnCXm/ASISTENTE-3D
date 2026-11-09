import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
for i in range(9):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=5.0, depth=0.25, location=(0, 0, i*3))
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=4.7, depth=24.0, location=(0, 0, 12.0))
