import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del terreno en metros
ancho = 20
alto = 15

# Crea un plano para el terreno
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))

# Selecciona el plano creado
bpy.context.active_object.name = "Terreno"

# Aplica una transformación de escala para que tenga las dimensiones correctas
bpy.ops.transform.resize(value=(ancho, alto, 0.01), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

# Crea un material de césped
mat_cesped = bpy.data.materials.new(name="Césped")
mat_cesped.use_nodes = True

# Accede a los nodos del material
nodes = mat_cesped.node_tree.nodes

# Agrega un nodo de color y lo configura para el verde del césped
nodes["Principio Color"].inputs[1].default_value = (0, 1, 0, 1)

# Agrega un nodo de textura y lo configura para una textura de césped
tex_cesped = nodes.new(type='ShaderNodeTexImage')
tex_cesped.image = bpy.data.images.load("path/to/cesped_texture.jpg")
nodes["Principio Color"].inputs[0].default_value = (1, 1, 1, 1)

# Conecta los nodos
mat_cesped.node_tree.links.new(nodes["Principio Color"].outputs[0], nodes["Glossy BSDF"].inputs[0])

# Aplica el material al terreno
bpy.context.active_object.data.materials.append(mat_cesped)