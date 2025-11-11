import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

base_x = 8.0
base_y = 6.0
altura_cumbrera = 2.0
alero = 0.5
grosor_cubierta = 0.2

# Calcular coordenadas de los vértices
# Puntos bajos del alero
v0 = (-base_x/2 - alero, -base_y/2 - alero, 0)
v1 = ( base_x/2 + alero, -base_y/2 - alero, 0)
v2 = ( base_x/2 + alero,  base_y/2 + alero, 0)
v3 = (-base_x/2 - alero,  base_y/2 + alero, 0)
# Puntos altos de la cumbrera
v4 = ( -base_x/2 - alero, 0, altura_cumbrera)
v5 = (  base_x/2 + alero, 0, altura_cumbrera)

verts = [v0, v1, v5, v4, v3, v2]
faces = [(0, 1, 5, 4), (4, 5, 2, 3)]

# Crear mesh y objeto
mesh = bpy.data.meshes.new(name="MallaCubierta")
obj = bpy.data.objects.new("CubiertaDosAguas", mesh)

# Vincular objeto a la escena
scene = bpy.context.scene
scene.collection.objects.link(obj)

# Asignar vértices y caras
mesh.from_pydata(verts, [], faces)
mesh.update(calc_edges=True)

# Darle grosor con un modificador
bpy.context.view_layer.objects.active = obj
mod = obj.modifiers.new(name='Solidify', type='SOLIDIFY')
mod.thickness = grosor_cubierta