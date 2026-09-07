import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá de tela gris
sofa = bpy.data.objects.new("Sofa", None)
bpy.context.collection.objects.link(sofa)

sofa_mesh = bpy.data.meshes.new(name="SofaMesh")
sofa_obj = bpy.data.objects.new("SofaObj", sofa_mesh)

# Definir la geometría del sofá
sofa_verts = [
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

sofa_mesh.from_pydata(sofa_verts, sofa_edges, sofa_faces)
sofa_mesh.update()

# Colocar el sofá en la escena
sofa.location = (1.5, -2, 0)

# Crear la mesa de centro de madera de nogal
table = bpy.data.objects.new("Table", None)
bpy.context.collection.objects.link(table)

table_mesh = bpy.data.meshes.new(name="TableMesh")
table_obj = bpy.data.objects.new("TableObj", table_mesh)

# Definir la geometría de la mesa
table_verts = [
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

table_mesh.from_pydata(table_verts, table_edges, table_faces)
table_mesh.update()

# Colocar la mesa en la escena
table.location = (1.5, -1, 0)

if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])