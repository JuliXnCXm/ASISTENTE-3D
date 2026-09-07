import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá modular
sofa = bpy.data.objects.new(name="Sofa", object_data=None)
bpy.context.collection.objects.link(sofa)

sofa_mesh = bpy.data.meshes.new(name="SofaMesh")
sofa_obj = bpy.data.objects.new(name="SofaObj", object_data=sofa_mesh)

# Definir la geometría del sofá
sofa_verts = [
    (-2, -1.5, 0), (2, -1.5, 0), (2, 1.5, 0), (-2, 1.5, 0),
    (-3, -1.5, 0), (-3, 1.5, 0), (3, -1.5, 0), (3, 1.5, 0)
]
sofa_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (6, 7), (7, 8), (8, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]
sofa_faces = [
    (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)
]

sofa_mesh.from_pydata(sofa_verts, sofa_edges, sofa_faces)
sofa_mesh.update()

bpy.context.collection.objects.link(sofa_obj)

# Aplicar modificador de esfera
bpy.ops.object.select_all(action='DESELECT')
sofa_obj.select_set(True)
bpy.context.view_layer.objects.active = sofa_obj
bpy.ops.object.modifier_add(type='SUBSURF')
bpy.ops.object.shade_smooth()

# Crear la alfombra
rug = bpy.data.meshes.new(name="RugMesh")
rug_obj = bpy.data.objects.new(name="Rug", object_data=rug)

rug_verts = [
    (-3, -2.5, 0), (3, -2.5, 0), (3, 2.5, 0), (-3, 2.5, 0)
]
rug_edges = [(i, i+1) for i in range(len(rug_verts)-1)] + [(len(rug_verts)-1, 0)]
rug_faces = [(0, 1, 2, 3)]

rug.from_pydata(rug_verts, rug_edges, rug_faces)
rug.update()

bpy.context.collection.objects.link(rug_obj)

# Aplicar modificador de esfera a la alfombra
bpy.ops.object.select_all(action='DESELECT')
rug_obj.select_set(True)
bpy.context.view_layer.objects.active = rug_obj
bpy.ops.object.modifier_add(type='SUBSURF')
bpy.ops.object.shade_smooth()

# Crear la estantería de diseño irregular
shelf = bpy.data.meshes.new(name="ShelfMesh")
shelf_obj = bpy.data.objects.new(name="Shelf", object_data=shelf)

shelf_verts = [
    (-1, -0.5, 0), (1, -0.5, 0), (1, 0.5, 0), (-1, 0.5, 0),
    (-2, -0.5, 0), (-2, 0.5, 0), (2, -0.5, 0), (2, 0.5, 0)
]
shelf_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (6, 7), (7, 8), (8, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]
shelf_faces = [
    (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)
]

shelf.from_pydata(shelf_verts, shelf_edges, shelf_faces)
shelf.update()

bpy.context.collection.objects.link(shelf_obj)

# Aplicar modificador de esfera a la estantería
bpy.ops.object.select_all(action='DESELECT')
shelf_obj.select_set(True)
bpy.context.view_layer.objects.active = shelf_obj
bpy.ops.object.modifier_add(type='SUBSURF')
bpy.ops.object.shade_smooth()

# Alinear y posicionar los objetos
sofa.location = (0, 0, -1.5)
rug.location = (0, 0, -2)
shelf.location = (-3, 0, -1)

# Guardar la escena si se especifica BLEND_OUT
if 'BLEND_OUT' in bpy.context.scene:
    out_path = bpy.context.scene['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=out_path)