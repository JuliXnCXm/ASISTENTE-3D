import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá de cuero
sofa = bpy.data.objects.new(name="Sofa", object_data=None)
bpy.context.collection.objects.link(sofa)

sofa_mesh = bpy.data.meshes.new(name="SofaMesh")
sofa_object = bpy.data.objects.new("SofaObject", sofa_mesh)

# Definir la geometría del sofá
sofa_vertices = [
    (-1, -0.5, 0), (1, -0.5, 0), (1, 0.5, 0), (-1, 0.5, 0),
    (-1, -0.5, 0.2), (1, -0.5, 0.2), (1, 0.5, 0.2), (-1, 0.5, 0.2)
]
sofa_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]
sofa_faces = [
    (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6),
    (3, 0, 4, 7)
]

sofa_mesh.from_pydata(sofa_vertices, sofa_edges, sofa_faces)
sofa_mesh.update()

# Crear la mesa de centro
table = bpy.data.objects.new(name="Table", object_data=None)
bpy.context.collection.objects.link(table)

table_mesh = bpy.data.meshes.new(name="TableMesh")
table_object = bpy.data.objects.new("TableObject", table_mesh)

# Definir la geometría de la mesa
table_vertices = [
    (-0.5, -0.25, 0), (0.5, -0.25, 0), (0.5, 0.25, 0), (-0.5, 0.25, 0),
    (-0.5, -0.25, 0.1), (0.5, -0.25, 0.1), (0.5, 0.25, 0.1), (-0.5, 0.25, 0.1)
]
table_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]
table_faces = [
    (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6),
    (3, 0, 4, 7)
]

table_mesh.from_pydata(table_vertices, table_edges, table_faces)
table_mesh.update()

# Posicionar los objetos
sofa.location = (-1.5, -1, 0)
table.location = (1.5, 0, 0)

if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])