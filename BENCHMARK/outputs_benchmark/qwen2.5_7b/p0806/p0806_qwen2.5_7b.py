import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá de tres plazas
sofa = bpy.data.objects.new(name="Sofa", object_data=None)
bpy.context.collection.objects.link(sofa)

bpy.ops.mesh.primitive_cube_add(location=(0, 0, -1))
sofa_mesh = bpy.context.object
sofa_mesh.scale = (2, 1.5, 0.8)  # Ajustar el tamaño para un sofá de tres plazas

# Aplicar material gris al sofá
material_sofa = bpy.data.materials.new(name="SofaMaterial")
material_sofa.use_nodes = True
nodes = material_sofa.node_tree.nodes
links = material_sofa.node_tree.links
output_node = nodes["Material Output"]
principled_bsdf = nodes["Principled BSDF"]

links.clear()
links.new(principled_bsdf.inputs['Base Color'], output_node.outputs['BSDF'])

material_sofa.diffuse_color = (0.5, 0.5, 0.5, 1)  # Gris
sofa_mesh.data.materials.append(material_sofa)

# Crear la mesa de centro
table = bpy.data.objects.new(name="Table", object_data=None)
bpy.context.collection.objects.link(table)

bpy.ops.mesh.primitive_cube_add(location=(0, -2.5, -1))
table_mesh = bpy.context.object
table_mesh.scale = (1.5, 1.5, 0.3)  # Ajustar el tamaño para una mesa de centro

# Aplicar material madera al sofá
material_table = bpy.data.materials.new(name="TableMaterial")
material_table.use_nodes = True
nodes = material_table.node_tree.nodes
links = material_table.node_tree.links
output_node = nodes["Material Output"]
principled_bsdf = nodes["Principled BSDF"]

links.clear()
links.new(principled_bsdf.inputs['Base Color'], output_node.outputs['BSDF'])

material_table.diffuse_color = (0.5, 0.35, 0.18, 1)  # Madera nogal
table_mesh.data.materials.append(material_table)

# Posicionar la mesa de centro frente al sofá
bpy.context.view_layer.objects.active = sofa_mesh
sofa_mesh.select_set(True)
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
bpy.ops.transform.resize(value=(1, 1, 1))
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

# Posicionar la mesa de centro
table.location = (0, -2.5, -1)

# Guardar el archivo .blend si existe BLEND_OUT
if "BLEND_OUT" in bpy.context.scene:
    blend_out_path = bpy.context.scene["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)