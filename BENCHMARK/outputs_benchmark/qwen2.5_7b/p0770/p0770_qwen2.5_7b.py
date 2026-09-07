import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá de tres plazas de tela gris
sofa = bpy.data.objects.new("Sofa", None)
bpy.context.collection.objects.link(sofa)

# Definir las geometría del sofá (sencillo cubo para demostración)
sofa_mesh = bpy.data.meshes.new(name="SofaMesh")
sofa_object = bpy.data.objects.new("SofaObject", sofa_mesh)
bpy.context.collection.objects.link(sofa_object)

sofa_vertices = [
    (-1, -0.5, 0), (1, -0.5, 0), (1, 0.5, 0), (-1, 0.5, 0),
    (-1, -0.5, 2), (1, -0.5, 2), (1, 0.5, 2), (-1, 0.5, 2)
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

# Asignar material de tela gris
material = bpy.data.materials.new(name="SofaMaterial")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

nodes.remove(nodes.get("Principled BSDF"))
emission_node = nodes.new(type='ShaderNodeEmission')
emission_node.inputs['Color'].default_value = (0.5, 0.5, 0.5, 1)
emission_node.inputs['Strength'].default_value = 1
links.new(emission_node.outputs['Emission'], nodes.get('Material Output').inputs['Surface'])

sofa_object.data.materials.append(material)

# Crear la mesa de centro de madera
table = bpy.data.objects.new("Table", None)
bpy.context.collection.objects.link(table)

# Definir las geometría de la mesa (sencillo cubo para demostración)
table_mesh = bpy.data.meshes.new(name="TableMesh")
table_object = bpy.data.objects.new("TableObject", table_mesh)
bpy.context.collection.objects.link(table_object)

table_vertices = [
    (-0.5, -0.25, 0), (0.5, -0.25, 0), (0.5, 0.25, 0), (-0.5, 0.25, 0),
    (-0.5, -0.25, 1), (0.5, -0.25, 1), (0.5, 0.25, 1), (-0.5, 0.25, 1)
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

# Asignar material de madera
material = bpy.data.materials.new(name="TableMaterial")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

nodes.remove(nodes.get("Principled BSDF"))
emission_node = nodes.new(type='ShaderNodeEmission')
emission_node.inputs['Color'].default_value = (0.5, 0.3, 0.1, 1)
emission_node.inputs['Strength'].default_value = 1
links.new(emission_node.outputs['Emission'], nodes.get('Material Output').inputs['Surface'])

table_object.data.materials.append(material)

# Posicionar el sofá y la mesa de centro
sofa.location = (0, -2, 0)
table.location = (0, 0.5, 0)

# Guardar el archivo .blend si existe BLEND_OUT
if 'BLEND_OUT' in bpy.context.scene:
    blend_out_path = bpy.context.scene['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)