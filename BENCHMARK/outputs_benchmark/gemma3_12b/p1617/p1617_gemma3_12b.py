import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones del terreno en metros
width = 20
length = 30
height = 0  # Terreno plano

# Crear la malla del terreno
bpy.ops.mesh.plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
terrain = bpy.context.object
terrain.scale = (width / 2, length / 2, 1)  # Escalar a las dimensiones deseadas
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True) # Aplicar la escala

# Crear el material de césped
material = bpy.data.materials.new(name="GrassMaterial")
material.use_nodes = True
nodes = material.node_tree.nodes
links = material.node_tree.links

# Eliminar el nodo BSDF por defecto
for node in nodes:
    if node.type == 'BSDF_PRINCIPLED':
        nodes.remove(node)

# Agregar nodos
principled_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
grass_texture = nodes.new(type='ShaderNodeTexGrass')
color_ramp = nodes.new(type='ShaderNodeValToRGB')
background_node = nodes.new(type='ShaderNodeBackground')

# Configurar el nodo de textura de césped
grass_texture.inputs['Scale'].default_value = 1.0
grass_texture.inputs['Strength'].default_value = 1.0
grass_texture.inputs['Direction'].default_value = (1.0, 0.0, 0.0)

# Configurar el nodo de rampa de color
color_ramp.interpolation = 'LINEAR'
color_ramp.elements[0].position = 0.0
color_ramp.elements[0].color = (0.0, 0.5, 0.0, 1.0)  # Verde oscuro
color_ramp.elements[1].position = 1.0
color_ramp.elements[1].color = (0.0, 0.8, 0.0, 1.0)  # Verde brillante

# Conectar nodos
links.new(grass_texture.outputs['Color'], color_ramp.inputs['Fac'])
links.new(color_ramp.outputs['Color'], principled_bsdf.inputs['Base Color'])
links.new(principled_bsdf.outputs['BSDF'], material.node_tree.outputs['Surface'])

# Asignar el material al terreno
if terrain.data.materials:
    terrain.data.materials[0] = material
else:
    terrain.data.materials.append(material)

# Ajustar el nombre del objeto
terrain.name = "GardenTerrain"

# Guardar el archivo .blend si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)