import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho_base = 6.0
largo_base = 8.0
pendiente_grados = 30.0
espesor = 0.2
alero = 0.5

# Cálculos
ancho_total = ancho_base + 2 * alero
largo_total = largo_base + 2 * alero
pendiente_rad = math.radians(pendiente_grados)
altura_cumbrera = (ancho_total / 2) * math.tan(pendiente_rad)

# Vértices de un faldón
v0 = (-ancho_total / 2, -largo_total / 2, 0)
v1 = (0, -largo_total / 2, altura_cumbrera)
v2 = (0, largo_total / 2, altura_cumbrera)
v3 = (-ancho_total / 2, largo_total / 2, 0)
verts = [v0, v1, v2, v3]
faces = [(0, 1, 2, 3)]

# Crear el primer faldón
mesh_data = bpy.data.meshes.new('Faldon_Mesh')
mesh_data.from_pydata(verts, [], faces)
obj_faldon1 = bpy.data.objects.new('Faldon_Izquierdo', mesh_data)
scene.collection.objects.link(obj_faldon1)

# Solidificar el faldón
solidify_mod = obj_faldon1.modifiers.new(name='Solidify', type='SOLIDIFY')
solidify_mod.thickness = espesor

# Crear el segundo faldón duplicando y espejando
obj_faldon2 = obj_faldon1.copy()
obj_faldon2.data = obj_faldon1.data.copy()
obj_faldon2.name = 'Faldon_Derecho'
obj_faldon2.scale.x = -1
scene.collection.objects.link(obj_faldon2)

# Aplicar transformaciones y modificadores
for obj in [obj_faldon1, obj_faldon2]:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.modifier_apply(modifier=solidify_mod.name)

# Unir los dos faldones en un solo objeto
obj_faldon1.select_set(True)
obj_faldon2.select_set(True)
bpy.context.view_layer.objects.active = obj_faldon1
bpy.ops.object.join()
obj_faldon1.name = 'CubiertaDosAguas'