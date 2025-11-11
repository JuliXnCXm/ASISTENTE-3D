import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar escena
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo = 10.0
ancho = 6.0
alto_muro = 3.0
espesor_muro = 0.2
pendiente_grados = 30

# Crear 4 muros
locations_scales = [
    ((largo/2, 0, alto_muro/2), (espesor_muro/2, ancho/2, alto_muro/2)),
    ((-largo/2, 0, alto_muro/2), (espesor_muro/2, ancho/2, alto_muro/2)),
    ((0, ancho/2, alto_muro/2), (largo/2, espesor_muro/2, alto_muro/2)),
    ((0, -ancho/2, alto_muro/2), (largo/2, espesor_muro/2, alto_muro/2))
]
for loc, sca in locations_scales:
    bpy.ops.mesh.primitive_cube_add(location=loc)
    obj = bpy.context.object
    obj.scale = sca
    bpy.ops.object.transform_apply(scale=True)

# Calcular altura de la cumbrera
altura_cumbrera = alto_muro + (ancho / 2) * math.tan(math.radians(pendiente_grados))

# Vertices de la cubierta
v1 = (-largo/2, -ancho/2, alto_muro)
v2 = (largo/2, -ancho/2, alto_muro)
v3 = (largo/2, 0, altura_cumbrera)
v4 = (-largo/2, 0, altura_cumbrera)
v5 = (-largo/2, ancho/2, alto_muro)
v6 = (largo/2, ancho/2, alto_muro)

# Crear faldón 1
verts1 = [v1, v2, v3, v4]
faces1 = [(0, 1, 2, 3)]
mesh1 = bpy.data.meshes.new('Faldon1_Mesh')
obj1 = bpy.data.objects.new('Faldon1', mesh1)
mesh1.from_pydata(verts1, [], faces1)
mesh1.update()
scene.collection.objects.link(obj1)

# Crear faldón 2
verts2 = [v4, v3, v6, v5]
faces2 = [(0, 1, 2, 3)]
mesh2 = bpy.data.meshes.new('Faldon2_Mesh')
obj2 = bpy.data.objects.new('Faldon2', mesh2)
mesh2.from_pydata(verts2, [], faces2)
mesh2.update()
scene.collection.objects.link(obj2)