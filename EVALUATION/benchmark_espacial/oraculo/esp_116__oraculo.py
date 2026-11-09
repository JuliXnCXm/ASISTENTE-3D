import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
for i in range(7):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=8.0, depth=0.25, location=(0, 0, i*3))
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=7.7, depth=18.0, location=(0, 0, 9.0))
