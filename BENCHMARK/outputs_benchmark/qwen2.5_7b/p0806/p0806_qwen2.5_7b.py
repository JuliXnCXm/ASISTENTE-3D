import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá de tres plazas
sofa = bpy.data.objects.new(name="Sofa", object_data=None)
bpy.context.collection.objects.link(sofa)

# Definir la geometría del sofá (simplificada para este ejemplo)
sofa_mesh = bpy.data.meshes.new(name="SofaMesh")
sofa_object = bpy.data.objects.new("SofaObject", sofa_mesh)

verts_sofa = [
    (-1, -0.5, 0), (-1, 0.5, 0), (1, 0.5, 0), (1, -0.5, 0),
    (-0.8, -0.7, 0.2), (-0.8, 0.7, 0.2), (0.8, 0.7, 0.2), (0.8, -0.7, 0.2)
]
edges_sofa = []
faces_sofa = [
    [0, 1, 3, 2], 
    [4, 5, 7, 6],
    [0, 1, 5, 4],
    [2, 3, 7, 6],
    [0, 2, 6, 4],
    [1, 3, 7, 5]
]

sofa_mesh.from_pydata(verts_sofa, edges_sofa, faces_sofa)
sofa_mesh.update()

# Asignar material al sofá (tela gris)
material_sofa = bpy.data.materials.new(name="SofaMaterial")
material_sofa.diffuse_color = (0.537255, 0.537255, 0.537255, 1)
sofa_mesh.materials.append(material_sofa)

# Crear la mesa de centro
table = bpy.data.objects.new(name="Table", object_data=None)
bpy.context.collection.objects.link(table)

# Definir la geometría de la mesa (cubo simplificado)
table_mesh = bpy.data.meshes.new(name="TableMesh")
table_object = bpy.data.objects.new("TableObject", table_mesh)

verts_table = [
    (-0.5, -0.25, 0), (-0.5, 0.25, 0), (0.5, 0.25, 0), (0.5, -0.25, 0)
]
edges_table = []
faces_table = [
    [0, 1, 3, 2]
]

table_mesh.from_pydata(verts_table, edges_table, faces_table)
table_mesh.update()

# Asignar material a la mesa (madera nogal)
material_table = bpy.data.materials.new(name="TableMaterial")
material_table.diffuse_color = (0.647059, 0.388235, 0.184314, 1)
table_mesh.materials.append(material_table)

# Posicionar el sofá y la mesa
sofa.location = (-3, 0, -1)
table.location = (3, 0, -1)

if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])