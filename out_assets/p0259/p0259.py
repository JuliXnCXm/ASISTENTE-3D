import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

largo = 10.0
ancho = 10.0
altura_max = 2.0
espesor = 0.15
nx = 32
ny = 32

# Malla de paraboloide (sin NURBS, sin bmesh)
verts = []
for iy in range(ny+1):
    y = (iy/ny - 0.5) * ancho
    for ix in range(nx+1):
        x = (ix/nx - 0.5) * largo
        z = altura_max * (1.0 - (2*x/largo)**2)
        verts.append((x, y, z))

faces = []
row = nx + 1
for iy in range(ny):
    for ix in range(nx):
        a = iy*row + ix
        b = a + 1
        c = a + row
        d = c + 1
        faces.append([a, b, d, c])

mesh = bpy.data.meshes.new("CubiertaParabolica")
mesh.from_pydata(verts, [], faces)
mesh.update()
obj = bpy.data.objects.new("CubiertaParabolica", mesh)
bpy.context.collection.objects.link(obj)

# Espesor con Solidify
mod = obj.modifiers.new(name="Espesor", type='SOLIDIFY')
mod.thickness = espesor
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
bpy.ops.object.modifier_apply(modifier=mod.name)
