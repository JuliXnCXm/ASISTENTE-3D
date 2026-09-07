import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá
sofa = bpy.data.objects.new(name="Sofa", object_data=None)
bpy.context.collection.objects.link(sofa)

sofa_mesh = bpy.data.meshes.new(name="SofaMesh")
sofa_obj = bpy.data.objects.new(name="Sofa", object_data=sofa_mesh)

# Definir la geometría del sofá (3 plazas, tapizado en tela gris)
sofa_vertices = [
    (-1.0, -0.5, 0.0), (-1.0, 0.5, 0.0), (-1.0, 0.8, 0.2),
    (0.0, -0.5, 0.0), (0.0, 0.5, 0.0), (0.0, 0.8, 0.2),
    (1.0, -0.5, 0.0), (1.0, 0.5, 0.0), (1.0, 0.8, 0.2)
]

sofa_faces = [
    (0, 3, 6), (3, 7, 4), (4, 1, 6), (6, 9, 7),
    (7, 5, 8), (5, 2, 8), (8, 9, 1), (9, 6, 3)
]

sofa_mesh.from_pydata(sofa_vertices, [], sofa_faces)
sofa_mesh.update()

# Asignar material al sofá
material = bpy.data.materials.new(name="SofaMaterial")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

nodes.remove(nodes.get('Principled BSDF'))
output_node = nodes.new(type='ShaderNodeOutputMaterial')
emission_node = nodes.new(type='ShaderNodeEmission')

emission_node.inputs['Color'].default_value = (0.5, 0.5, 0.5, 1)
emission_node.inputs['Strength'].default_value = 1

links.new(emission_node.outputs['Emission'], output_node.inputs['Surface'])

sofa_obj.data.materials.append(material)

# Crear la mesa de centro
table = bpy.data.objects.new(name="Table", object_data=None)
bpy.context.collection.objects.link(table)

table_mesh = bpy.data.meshes.new(name="TableMesh")
table_obj = bpy.data.objects.new(name="Table", object_data=table_mesh)

# Definir la geometría de la mesa (madera de nogal)
table_vertices = [
    (-0.5, -0.2, 0.0), (-0.5, 0.2, 0.0), (-0.3, 0.2, 0.1),
    (-0.3, -0.2, 0.1), (0.3, -0.2, 0.1), (0.3, 0.2, 0.1),
    (0.5, -0.2, 0.0), (0.5, 0.2, 0.0)
]

table_faces = [
    (0, 4, 7), (7, 6, 3), (3, 2, 1), (1, 5, 4),
    (4, 0, 3), (3, 7, 6), (6, 5, 2), (2, 1, 0)
]

table_mesh.from_pydata(table_vertices, [], table_faces)
table_mesh.update()

# Asignar material a la mesa
material = bpy.data.materials.new(name="TableMaterial")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

nodes.remove(nodes.get('Principled BSDF'))
output_node = nodes.new(type='ShaderNodeOutputMaterial')
emission_node = nodes.new(type='ShaderNodeEmission')

emission_node.inputs['Color'].default_value = (0.4, 0.25, 0.1, 1)
emission_node.inputs['Strength'].default_value = 1

links.new(emission_node.outputs['Emission'], output_node.inputs['Surface'])

table_obj.data.materials.append(material)

# Posicionar los objetos
sofa.location = (0, -3, 0)
table.location = (0, 2, 0.1)

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])