import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la cama
ancho = 1.6
largo = 2.0
alto = 0.5

# Crea el colchón
colchon = bpy.data.meshes.new("Colchon")
colchon_objeto = bpy.data.objects.new("Colchon", colchon)
bpy.context.collection.objects.link(colchon_objeto)

verts = [
    (-ancho/2, -largo/2, 0),
    (ancho/2, -largo/2, 0),
    (ancho/2, largo/2, 0),
    (-ancho/2, largo/2, 0)
]

faces = [
    (0, 1, 2, 3)
]

colchon.from_pydata(verts, [], faces)
bpy.context.collection.objects.link(colchon_objeto)

# Crea la estructura de madera
estructura = bpy.data.meshes.new("Estructura")
estructura_objeto = bpy.data.objects.new("Estructura", estructura)
bpy.context.collection.objects.link(estructura_objeto)

verts_estructura = [
    (-ancho/2, -largo/2, alto),
    (ancho/2, -largo/2, alto),
    (ancho/2, largo/2, alto),
    (-ancho/2, largo/2, alto)
]

faces_estructura = [
    (0, 1, 2, 3)
]

estructura.from_pydata(verts_estructura, [], faces_estructura)
bpy.context.collection.objects.link(estructura_objeto)

# Aplica materiales
colchon_material = bpy.data.materials.new("ColchonMaterial")
colchon_material.use_nodes = True
colchon_material.node_tree.nodes["Principled BSDF"].base_color = (1, 1, 1, 1)
colchon_objeto.data.materials.append(colchon_material)

estructura_material = bpy.data.materials.new("EstructuraMaterial")
estructura_material.use_nodes = True
estructura_material.node_tree.nodes["Principled BSDF"].base_color = (0.5, 0.2, 0.1, 1)
estructura_objeto.data.materials.append(estructura_material)

# Guarda el archivo .blend si se especifica la variable de entorno BLEND_OUT
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])