import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá
sofa = bpy.data.objects.new(name="Sofa", object_data=None)
bpy.context.collection.objects.link(sofa)

sofa_mesh = bpy.data.meshes.new(name="SofaMesh")
sofa_obj = bpy.data.objects.new("Sofa", sofa_mesh)
bpy.context.collection.objects.link(sofa_obj)

sofa_mesh.from_pydata(
    [(0, 1.5, -0.2), (3, 1.5, -0.2), (3, 1.5, 0.8), (0, 1.5, 0.8),
     (0, 0.5, 0.8), (3, 0.5, 0.8), (3, 0.5, -0.2), (0, 0.5, -0.2)],
    [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0)],
    [(0, 1, 2), (2, 3, 4), (4, 5, 6), (6, 7, 0)]
)
sofa_mesh.update()

material_sofa = bpy.data.materials.new(name="SofaMaterial")
material_sofa.use_nodes = True
nodes = material_sofa.node_tree.nodes
links = material_sofa.node_tree.links

nodes.remove(nodes.get('Principled BSDF'))
output_node = nodes.new(type='ShaderNodeOutputMaterial')
emission_node = nodes.new(type='ShaderNodeEmission')

emission_node.inputs['Color'].default_value = (0.5, 0.5, 0.5, 1)
emission_node.inputs['Strength'].default_value = 1

links.new(emission_node.outputs['Emission'], output_node.inputs['Surface'])

sofa_obj.data.materials.append(material_sofa)

# Crear la mesa de centro
table = bpy.data.objects.new(name="Table", object_data=None)
bpy.context.collection.objects.link(table)

table_mesh = bpy.data.meshes.new(name="TableMesh")
table_obj = bpy.data.objects.new("Table", table_mesh)
bpy.context.collection.objects.link(table_obj)

table_mesh.from_pydata(
    [(-0.5, 1.2, -0.1), (0.5, 1.2, -0.1), (0.5, 1.2, 0.3), (-0.5, 1.2, 0.3),
     (-0.5, 0.8, 0.3), (0.5, 0.8, 0.3), (0.5, 0.8, -0.1), (-0.5, 0.8, -0.1)],
    [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0)],
    [(0, 1, 2), (2, 3, 0), (4, 5, 6), (6, 7, 4)]
)
table_mesh.update()

material_table = bpy.data.materials.new(name="TableMaterial")
material_table.use_nodes = True
nodes = material_table.node_tree.nodes
links = material_table.node_tree.links

nodes.remove(nodes.get('Principled BSDF'))
output_node = nodes.new(type='ShaderNodeOutputMaterial')
emission_node = nodes.new(type='ShaderNodeEmission')

emission_node.inputs['Color'].default_value = (0.7, 0.5, 0.3, 1)
emission_node.inputs['Strength'].default_value = 1

links.new(emission_node.outputs['Emission'], output_node.inputs['Surface'])

table_obj.data.materials.append(material_table)

# Posicionar el sofá y la mesa
sofa.location = (0, -2, 0.5)
table.location = (0, 1, 0.3)

if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.context.scene['BLEND_OUT'])