import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la cama
ancho = 1.60
largo = 2.00

# Crea el marco superior de la cama (estructura de madera)
marco_superior = bpy.data.curves.new(name="Marco Superior", type='MESH')
marco_superior.dimensions = '2D'
marco_superior.fill_mode = 'FULL'

verts = [
    mathutils.Vector((-ancho/2, -largo/2)),
    mathutils.Vector((ancho/2, -largo/2)),
    mathutils.Vector((ancho/2, largo/2)),
    mathutils.Vector((-ancho/2, largo/2))
]

faces = [
    (0, 1, 2, 3)
]

marco_superior.data.from_pydata(verts, [], faces)
bpy.context.collection.objects.link(marco_superior)

# Crea el marco inferior de la cama
marco_inferior = bpy.data.curves.new(name="Marco Inferior", type='MESH')
marco_inferior.dimensions = '2D'
marco_inferior.fill_mode = 'FULL'

verts = [
    mathutils.Vector((-ancho/2, -largo/2)),
    mathutils.Vector((ancho/2, -largo/2)),
    mathutils.Vector((ancho/2, largo/2)),
    mathutils.Vector((-ancho/2, largo/2))
]

faces = [
    (0, 1, 2, 3)
]

marco_inferior.data.from_pydata(verts, [], faces)
bpy.context.collection.objects.link(marco_inferior)

# Crea el colchón
colchon = bpy.data.curves.new(name="Colchon", type='MESH')
colchon.dimensions = '2D'
colchon.fill_mode = 'FULL'

verts = [
    mathutils.Vector((-ancho/2, -largo/2)),
    mathutils.Vector((ancho/2, -largo/2)),
    mathutils.Vector((ancho/2, largo/2)),
    mathutils.Vector((-ancho/2, largo/2))
]

faces = [
    (0, 1, 2, 3)
]

colchon.data.from_pydata(verts, [], faces)

# Aplica la textura de colchón
colchon.active_material = bpy.data.materials.new(name="Colchon Material")
colchon.active_material.use_nodes = True

node_tree = colchon.active_material.node_tree
nodes = node_tree.nodes

nodes["Principio Color"].inputs['Color'].default_value = (1, 1, 1, 1) # Blanco

# Aplica la textura de madera al marco superior e inferior
marco_superior.active_material = bpy.data.materials.new(name="Marco Material")
marco_superior.active_material.use_nodes = True

node_tree = marco_superior.active_material.node_tree
nodes = node_tree.nodes

nodes["Principio Color"].inputs['Color'].default_value = (0.5, 0.2, 0.1, 1) # Madera de roble

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])