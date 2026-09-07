import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá de tela gris
sofa = bpy.data.objects.new(name="Sofa", object_data=None)
bpy.context.collection.objects.link(sofa)

sofa_mesh = bpy.data.meshes.new(name="SofaMesh")
sofa_obj = bpy.data.objects.new(name="Sofa", object_data=sofa_mesh)

# Definir la geometría del sofá (3 plazas)
sofa_vertices = [
    (-1, -0.5, 0), (-1, 0.5, 0), (-1, 1, 0),
    (0, -0.5, 0), (0, 0.5, 0), (0, 1, 0),
    (1, -0.5, 0), (1, 0.5, 0), (1, 1, 0)
]
sofa_edges = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5),
    (6, 7), (7, 8), (8, 9), (9, 6),
    (0, 6), (1, 7), (2, 8), (3, 9)
]

sofa_mesh.from_pydata(sofa_vertices, sofa_edges, [])
sofa_mesh.update()

# Asignar material al sofá
material = bpy.data.materials.new(name="SofaMaterial")
material.diffuse_color = (0.537, 0.486, 0.419, 1)  # Color gris
sofa_obj.data.materials.append(material)

# Crear la mesa de centro de madera de nogal
table = bpy.data.objects.new(name="Table", object_data=None)
bpy.context.collection.objects.link(table)

table_mesh = bpy.data.meshes.new(name="TableMesh")
table_obj = bpy.data.objects.new(name="Table", object_data=table_mesh)

# Definir la geometría de la mesa (rectangular)
table_vertices = [
    (-0.5, -0.25, 0), (-0.5, 0.25, 0), (0.5, 0.25, 0), (0.5, -0.25, 0)
]
table_edges = [(0, 1), (1, 2), (2, 3), (3, 0)]

table_mesh.from_pydata(table_vertices, table_edges, [])
table_mesh.update()

# Asignar material a la mesa
material = bpy.data.materials.new(name="TableMaterial")
material.diffuse_color = (0.647, 0.518, 0.298, 1)  # Color madera nogal
table_obj.data.materials.append(material)

# Posicionar el sofá y la mesa
sofa.location = (-3, 0, -0.1)
table.location = (0, 0, -0.1)

if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])