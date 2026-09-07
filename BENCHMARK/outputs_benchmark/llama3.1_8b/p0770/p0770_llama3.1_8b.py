import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las propiedades de la geometría
sofa_length = 2.5  # metros
sofa_width = 1.8   # metros
mesa_centro_length = 1.2  # metros
mesa_centro_width = 0.6  # metros

# Crea el plano para el suelo
bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, -0.01))

# Crea el sofá
sofa_mesh = bpy.data.meshes.new("SofaMesh")
sofa_obj = bpy.data.objects.new("Sofa", sofa_mesh)

# Define los vértices del sofá
vertices = [
    (-sofa_length/2, -sofa_width/2, 0),
    (sofa_length/2, -sofa_width/2, 0),
    (sofa_length/2, sofa_width/2, 0),
    (-sofa_length/2, sofa_width/2, 0)
]

# Define las caras del sofá
faces = [
    (0, 1, 2, 3)  # cara superior
]

# Define los bordes del sofá
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0)
]

# Crea el polígono de la geometría del sofá
sofa_mesh.from_pydata(vertices, edges, faces)
sofa_obj.data = sofa_mesh

# Aplica la transformación para colocar el sofá en la escena
sofa_obj.location = (0, 0, 0)

# Agrega el sofá a la escena
bpy.context.collection.objects.link(sofa_obj)

# Crea la mesa de centro
mesa_centro_mesh = bpy.data.meshes.new("MesaCentroMesh")
mesa_centro_obj = bpy.data.objects.new("MesaCentro", mesa_centro_mesh)

# Define los vértices de la mesa de centro
vertices_mesa_centro = [
    (-mesa_centro_length/2, -mesa_centro_width/2, 0),
    (mesa_centro_length/2, -mesa_centro_width/2, 0),
    (mesa_centro_length/2, mesa_centro_width/2, 0),
    (-mesa_centro_length/2, mesa_centro_width/2, 0)
]

# Define las caras de la mesa de centro
faces_mesa_centro = [
    (0, 1, 2, 3)  # cara superior
]

# Define los bordes de la mesa de centro
edges_mesa_centro = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0)
]

# Crea el polígono de la geometría de la mesa de centro
mesa_centro_mesh.from_pydata(vertices_mesa_centro, edges_mesa_centro, faces_mesa_centro)
mesa_centro_obj.data = mesa_centro_mesh

# Aplica la transformación para colocar la mesa de centro en la escena
mesa_centro_obj.location = (0, 0, -0.1)

# Agrega la mesa de centro a la escena
bpy.context.collection.objects.link(mesa_centro_obj)

# Guarda el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])