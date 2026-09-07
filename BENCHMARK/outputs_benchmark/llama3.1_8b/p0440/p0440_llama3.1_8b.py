import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Establece las unidades en metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Crea el colchón blanco
colchon = bpy.data.objects.new('Colchon', bpy.data.meshes.new('Colchon'))
colchon.location = mathutils.Vector((0, 0, 0))
colchon.scale = (2.1, 1.5, 0.3)

# Crea la geometría del colchón
verts = [
    (-1.05, -0.75, 0),
    (1.05, -0.75, 0),
    (1.05, 0.75, 0),
    (-1.05, 0.75, 0)
]
faces = [
    (0, 1, 2, 3)
]

colchon.data.from_pydata(verts, [], faces)
colchon.data.update()

# Crea la estructura de madera de roble
estructura = bpy.data.objects.new('Estructura', bpy.data.meshes.new('Estructura'))
estructura.location = mathutils.Vector((0, 0, 0))
estructura.scale = (2.1, 1.5, 0.3)

# Crea la geometría de la estructura
verts = [
    (-1.05, -0.75, 0),
    (1.05, -0.75, 0),
    (1.05, 0.75, 0),
    (-1.05, 0.75, 0)
]
faces = [
    (0, 1, 2, 3)
]

estructura.data.from_pydata(verts, [], faces)
estructura.data.update()

# Agrega los objetos a la escena
bpy.context.collection.objects.link(colchon)
bpy.context.collection.objects.link(estructura)

# Aplica materiales al colchón y estructura
colchon.active_material = bpy.data.materials.new('ColchonMaterial')
colchon.active_material.use_nodes = True

estructura.active_material = bpy.data.materials.new('EstructuraMaterial')
estructura.active_material.use_nodes = True

# Crea materiales de colores para el colchón y la estructura
colchon_mat = colchon.active_material.node_tree.nodes['Principio de base'].inputs[0].default_value
estructura_mat = estructura.active_material.node_tree.nodes['Principio de base'].inputs[0].default_value

# Aplica materiales a los objetos
colchon.active_material.node_tree.nodes['Principio de base'].inputs[0].default_value = (1, 1, 1, 1)
estructura.active_material.node_tree.nodes['Principio de base'].inputs[0].default_value = (0.5, 0.2, 0.1, 1)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])