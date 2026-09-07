import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones del terreno y la casa
terreno_size = (25, 20)
casa_size = (12, 9)

# Crear el terreno de césped
ground_mesh = bpy.data.meshes.new(name="Ground")
ground_obj = bpy.data.objects.new("Ground", ground_mesh)
bpy.context.collection.objects.link(ground_obj)

ground_mesh.from_pydata([(0, 0, 0), (terreno_size[0], 0, 0), (terreno_size[0], terreno_size[1], 0), (0, terreno_size[1], 0)], [], [])
ground_mesh.update()

# Crear la casa
house_mesh = bpy.data.meshes.new(name="House")
house_obj = bpy.data.objects.new("House", house_mesh)
bpy.context.collection.objects.link(house_obj)

# Definir las paredes de la casa
wall_verts = [
    (-casa_size[0]/2, -casa_size[1]/2, 0), 
    (casa_size[0]/2, -casa_size[1]/2, 0), 
    (casa_size[0]/2, casa_size[1]/2, 0), 
    (-casa_size[0]/2, casa_size[1]/2, 0)
]

wall_edges = [(i, i+1) for i in range(len(wall_verts)-1)] + [(len(wall_verts)-1, 0)]

# Agregar techo
roof_verts = [
    (casa_size[0]/2, -casa_size[1]/2, 3), 
    (-casa_size[0]/2, -casa_size[1]/2, 3), 
    (-casa_size[0]/2, casa_size[1]/2, 3), 
    (casa_size[0]/2, casa_size[1]/2, 3)
]

roof_edges = [(i, i+1) for i in range(len(roof_verts)-1)] + [(len(roof_verts)-1, 0)]

house_mesh.from_pydata(wall_verts + roof_verts, wall_edges + roof_edges, [])
house_mesh.update()

# Posicionar la casa en el centro del terreno
house_obj.location = (terreno_size[0]/2 - casa_size[0]/2, terreno_size[1]/2 - casa_size[1]/2, 3)

# Crear un árbol en el jardín frontal
tree_mesh = bpy.data.meshes.new(name="Tree")
tree_obj = bpy.data.objects.new("Tree", tree_mesh)
bpy.context.collection.objects.link(tree_obj)

# Definir la geometría del tronco y las ramas
trunk_verts = [(0, 0, 1), (0, -0.5, 2)]
trunk_edges = [(i, i+1) for i in range(len(trunk_verts)-1)]

branch_verts = [
    (-0.3, -0.4, 3), 
    (-0.3, -0.6, 4), 
    (0.3, -0.6, 4), 
    (0.3, -0.4, 3)
]

branch_edges = [(i, i+1) for i in range(len(branch_verts)-1)]

tree_mesh.from_pydata(trunk_verts + branch_verts, trunk_edges + branch_edges, [])
tree_mesh.update()

# Posicionar el árbol en la parte frontal del terreno
tree_obj.location = (terreno_size[0]/2 - casa_size[0]/2 - 3, terreno_size[1]/2 - 5, 4)

if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])