import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el terreno plano
terreno = bpy.data.meshes.new(name="Terreno")
obj_terreno = bpy.data.objects.new("Terreno", terreno)
bpy.context.collection.objects.link(obj_terreno)

# Definir la geometría del terreno
verts = [(0, 0, 0), (20, 0, 0), (20, 15, 0), (0, 15, 0)]
edges = []
faces = [(0, 1, 2, 3)]

# Asignar la geometría al objeto
terreno.from_pydata(verts, edges, faces)
terreno.update()

# Crear material de césped
material = bpy.data.materials.new(name="Césped")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

# Eliminar el nodo base_color
nodes.remove(nodes.get("Base Color"))

# Agregar un nuevo nodo emission y conectarlo al output
emission_node = nodes.new(type='ShaderNodeEmission')
emission_node.inputs['Color'].default_value = (0.2, 0.65, 0.1, 1)  # Verde claro
emission_node.inputs['Strength'].default_value = 1

links.new(emission_node.outputs['Emission'], nodes.get("Material Output").inputs['Surface'])

# Asignar el material al terreno
obj_terreno.data.materials.append(material)

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])