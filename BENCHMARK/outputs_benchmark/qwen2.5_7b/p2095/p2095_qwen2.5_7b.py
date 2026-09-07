import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá modular
sofa = bpy.data.objects.new(name="Sofa", object_data=None)
bpy.context.collection.objects.link(sofa)

sofa_mesh = bpy.data.meshes.new(name="SofaMesh")
sofa_obj = bpy.data.objects.new(name="Sofa", object_data=sofa_mesh)
bpy.context.collection.objects.link(sofa_obj)

sofa_mesh.from_pydata(
    [(0, 2.5, 0), (1.5, 3, 0), (4, 3, 0), (5.5, 2.5, 0), (6, 1, 0), (5.5, -0.5, 0), (4, -1, 0), (1.5, -0.5, 0)],
    [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0)],
    []
)
sofa_mesh.update()

# Aplicar modificador de subdivision
subdivision = sofa_obj.modifiers.new(name="Subdivision", type='SUBSURF')
subdivision.levels = 2

# Crear la alfombra
rug = bpy.data.objects.new(name="Rug", object_data=None)
bpy.context.collection.objects.link(rug)

rug_mesh = bpy.data.meshes.new(name="RugMesh")
rug_obj = bpy.data.objects.new(name="Rug", object_data=rug_mesh)
bpy.context.collection.objects.link(rug_obj)

rug_mesh.from_pydata(
    [(2, -1.5, 0), (3, -1, 0), (4, -1, 0), (5, -1.5, 0)],
    [],
    [(0, 1, 2, 3)]
)
rug_mesh.update()

# Crear la estantería
shelf = bpy.data.objects.new(name="Shelf", object_data=None)
bpy.context.collection.objects.link(shelf)

shelf_mesh = bpy.data.meshes.new(name="ShelfMesh")
shelf_obj = bpy.data.objects.new(name="Shelf", object_data=shelf_mesh)
bpy.context.collection.objects.link(shelf_obj)

shelf_mesh.from_pydata(
    [(2, -3.5, 0), (4, -3.5, 0), (4, -1.5, 0), (2, -1.5, 0)],
    [],
    [(0, 1, 2, 3)]
)
shelf_mesh.update()

# Aplicar modificador de bevel
bevel = shelf_obj.modifiers.new(name="Bevel", type='BEVEL')
bevel.width = 0.1

# Guardar la escena si se proporciona BLEND_OUT
if "BLEND_OUT" in bpy.context.scene:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.context.scene["BLEND_OUT"])