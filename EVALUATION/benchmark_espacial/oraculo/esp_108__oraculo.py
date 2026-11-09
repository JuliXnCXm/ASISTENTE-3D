import blender_arch as A
import bpy
import bmesh
import math

A.limpiar_escena()
casa = A.crear_casa_n_pisos('Casa', pisos=1, ancho=8, fondo=10, alto_piso=3, con_tejado=False)

me = bpy.data.meshes.new('TechoMono')
bm = bmesh.new()
pts = [(-0.3, -0.3), (8.3, -0.3), (8.3, 10.3), (-0.3, 10.3)]
hz = (4.61061584566772, 3.2, 3.2, 4.61061584566772)
bot = [bm.verts.new((x, y, 3.0)) for x, y in pts]
top = [bm.verts.new((x, y, z)) for (x, y), z in zip(pts, hz)]
bm.faces.new(bot[::-1]); bm.faces.new(top)
for i in range(4):
    j = (i + 1) % 4
    bm.faces.new((bot[i], bot[j], top[j], top[i]))
bm.normal_update(); bm.to_mesh(me); bm.free()
techo = bpy.data.objects.new('TechoMono', me)
bpy.context.collection.objects.link(techo)
