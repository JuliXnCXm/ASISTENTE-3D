import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el terreno plano
terreno = bpy.data.meshes.new(name="Terreno")
obj = bpy.data.objects.new("Terreno", terreno)
bpy.context.collection.objects.link(obj)

# Definir los vértices del terreno
verts = [
    (-10, -7.5, 0),
    (10, -7.5, 0),
    (10, 7.5, 0),
    (-10, 7.5, 0)
]

# Definir los caras del terreno
faces = [(0, 1, 2, 3)]

# Crear la geometría
terreno.from_pydata(verts, [], faces)
terreno.update()

# Asignar material de césped
material = bpy.data.materials.new(name="Césped")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

# Eliminar el nodo base_color y agregar un nuevo nodo
nodes.remove(nodes.get('Base Color'))
emission_node = nodes.new(type='ShaderNodeEmission')
emission_node.inputs['Color'].default_value = (0.2, 0.65, 0.1, 1)
emission_node.inputs['Strength'].default_value = 1

# Conectar el nodo de emisión al output
links.new(emission_node.outputs['Emission'], nodes.get('Material Output').inputs['Surface'])

obj.data.materials.append(material)

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if 'BLEND_OUT' in dir(bpy.app):
    bpy.ops.wm.save_as_mainfile(filepath=bpy.app.handlers.save_pre.properties.filepath)