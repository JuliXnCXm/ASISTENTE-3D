import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el terreno plano de césped
terreno = bpy.data.meshes.new(name="Césped")
obj_terreno = bpy.data.objects.new("Terreno_Césped", terreno)
bpy.context.collection.objects.link(obj_terreno)

# Definir la geometría del terreno
verts = [
    (-7.5, -5, 0),
    (7.5, -5, 0),
    (7.5, 5, 0),
    (-7.5, 5, 0)
]

edges = []
faces = [(0, 1, 2, 3)]

# Crear la mesh
terreno.from_pydata(verts, edges, faces)
terreno.update()

# Ajustar el tamaño del terreno a 15x10 metros
bpy.ops.object.select_all(action='DESELECT')
obj_terreno.select_set(True)
bpy.context.view_layer.objects.active = obj_terreno
bpy.ops.transform.resize(value=(15, 10, 1))

# Añadir un material verde para el césped
material = bpy.data.materials.new(name="Césped")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

nodes.clear()
emission_node = nodes.new(type='ShaderNodeEmission')
emission_node.inputs['Color'].default_value = (0.3, 1, 0.3, 1)
emission_node.inputs['Strength'].default_value = 2
output_node = nodes.new(type='ShaderNodeOutputMaterial')

links.new(emission_node.outputs['Emission'], output_node.inputs['Surface'])

obj_terreno.data.materials.append(material)

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if 'BLEND_OUT' in dir(bpy.app):
    bpy.ops.wm.save_as_mainfile(filepath=bpy.app.debug_path + "terreno_césped.blend")