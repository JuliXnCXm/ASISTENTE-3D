import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear un terreno plano de césped de 15x15 metros
bpy.ops.mesh.primitive_plane_add(size=15, location=(0, 0, 0))
plane = bpy.context.object

# Asignar un material verde al terreno
material = bpy.data.materials.new(name="Césped")
material.use_nodes = True
nodes = material.node_tree.nodes
nodes.clear()
output_node = nodes.new(type='ShaderNodeOutputMaterial')
bsdf_node = nodes.new(type='ShaderNodeBsdfDiffuse')
color_node = nodes.new(type='ShaderNodeRGB')
color_node.outputs['Color'].default_value = (0.4, 0.8, 0.2, 1)
nodes.links.new(bsdf_node.inputs['Color'], color_node.outputs['Color'])
nodes.links.new(output_node.inputs['Surface'], bsdf_node.outputs['BSDF'])

plane.data.materials.append(material)

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if 'BLEND_OUT' in bpy.context.scene:
    blend_out_path = bpy.context.scene[BLEND_OUT]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)