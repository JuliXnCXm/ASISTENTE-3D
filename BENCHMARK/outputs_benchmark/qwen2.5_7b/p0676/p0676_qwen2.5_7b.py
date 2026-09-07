import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá de tres plazas de tela gris
sofa = bpy.data.objects.new("Sofa", None)
bpy.context.collection.objects.link(sofa)

# Definir las geometría del sofá (simplificado para ejemplo)
sofa_mesh = bpy.data.meshes.new(name="SofaMesh")
sofa_object = bpy.data.objects.new("SofaObject", sofa_mesh)

verts_sofa = [
    (-1, -0.5, 0), (-1, 0.5, 0), (1, 0.5, 0), (1, -0.5, 0),
    (-0.5, -1, 0.2), (-0.5, 1, 0.2), (0.5, 1, 0.2), (0.5, -1, 0.2)
]
edges_sofa = []
faces_sofa = [
    (0, 1, 3, 2),
    (4, 5, 7, 6),
    (0, 1, 5, 4),
    (2, 3, 7, 6),
    (0, 2, 6, 4),
    (1, 3, 7, 5)
]

sofa_mesh.from_pydata(verts_sofa, edges_sofa, faces_sofa)
sofa_mesh.update()

# Asignar material de tela gris
material = bpy.data.materials.new(name="SofaMaterial")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

nodes.clear()
emission_node = nodes.new(type='ShaderNodeEmission')
emission_node.inputs['Color'].default_value = (0.5, 0.5, 0.5, 1)
emission_node.inputs['Strength'].default_value = 1
output_node = nodes.new(type='ShaderNodeOutputMaterial')

links.new(emission_node.outputs['Emission'], output_node.inputs['Surface'])

sofa_object.data.materials.append(material)

# Crear la mesa de centro de madera de roble
table = bpy.data.objects.new("Table", None)
bpy.context.collection.objects.link(table)

# Definir las geometría de la mesa (simplificado para ejemplo)
table_mesh = bpy.data.meshes.new(name="TableMesh")
table_object = bpy.data.objects.new("TableObject", table_mesh)

verts_table = [
    (-0.5, -0.25, 0), (-0.5, 0.25, 0), (0.5, 0.25, 0), (0.5, -0.25, 0),
    (0, 0, 0.1)
]
edges_table = []
faces_table = [
    (0, 1, 3, 2),
    (4, 0, 2, 4),
    (4, 1, 3, 4)
]

table_mesh.from_pydata(verts_table, edges_table, faces_table)
table_mesh.update()

# Asignar material de madera
material = bpy.data.materials.new(name="TableMaterial")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

nodes.clear()
emission_node = nodes.new(type='ShaderNodeBsdfDiffuse')
emission_node.inputs['Color'].default_value = (0.5, 0.35, 0.18, 1)
output_node = nodes.new(type='ShaderNodeOutputMaterial')

links.new(emission_node.outputs['BSDF'], output_node.inputs['Surface'])

table_object.data.materials.append(material)

# Posicionar el sofá y la mesa
sofa.location = (0, -2, 0.5)
table.location = (0, 1, 0.3)

if "BLEND_OUT" in bpy.context.scene:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.context.scene["BLEND_OUT"])