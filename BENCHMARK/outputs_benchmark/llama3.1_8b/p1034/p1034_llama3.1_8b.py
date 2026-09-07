import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las propiedades del objeto
width = 1.6  # Ancho en metros
length = 2.0  # Longitud en metros
thickness = 0.05  # Espesor de la madera en metros

# Crea el marco superior de la cama
bpy.ops.mesh.primitive_cube_add(size=width, location=(0, 0, length/2 + thickness))
obj_superior = bpy.context.active_object
obj_superior.name = "Cama Superior"
obj_superior.scale[1] = 0.01  # Reduce el tamaño en la dirección Y para simular una madera delgada

# Crea el marco inferior de la cama
bpy.ops.mesh.primitive_cube_add(size=width, location=(0, 0, -length/2))
obj_inferior = bpy.context.active_object
obj_inferior.name = "Cama Inferior"
obj_inferior.scale[1] = 0.01  # Reduce el tamaño en la dirección Y para simular una madera delgada

# Crea las patas de la cama
bpy.ops.mesh.primitive_cube_add(size=thickness, location=(-width/2, -length/2, length/2))
obj_pata1 = bpy.context.active_object
obj_pata1.name = "Pata 1"
obj_pata1.scale[0] = 0.01  # Reduce el tamaño en la dirección X para simular una madera delgada

bpy.ops.mesh.primitive_cube_add(size=thickness, location=(-width/2, length/2, length/2))
obj_pata2 = bpy.context.active_object
obj_pata2.name = "Pata 2"
obj_pata2.scale[0] = 0.01  # Reduce el tamaño en la dirección X para simular una madera delgada

bpy.ops.mesh.primitive_cube_add(size=thickness, location=(width/2, -length/2, length/2))
obj_pata3 = bpy.context.active_object
obj_pata3.name = "Pata 3"
obj_pata3.scale[0] = 0.01  # Reduce el tamaño en la dirección X para simular una madera delgada

bpy.ops.mesh.primitive_cube_add(size=thickness, location=(width/2, length/2, length/2))
obj_pata4 = bpy.context.active_object
obj_pata4.name = "Pata 4"
obj_pata4.scale[0] = 0.01  # Reduce el tamaño en la dirección X para simular una madera delgada

# Crea el colchón de tela blanca
bpy.ops.mesh.primitive_plane_add(size=width, location=(0, 0, length/2))
obj_colchon = bpy.context.active_object
obj_colchon.name = "Colchón"
obj_colchon.scale[1] = 0.01  # Reduce el tamaño en la dirección Y para simular una tela delgada

# Aplica materiales a los objetos
mat_roble = bpy.data.materials.new(name="Madera de Roble")
mat_roble.use_nodes = True
mat_roble.node_tree.nodes["Principio de Diffuso"].inputs[0].default_value = (1, 1, 1, 1)
bpy.context.active_object.data.materials.append(mat_roble)

mat_tela = bpy.data.materials.new(name="Tela Blanca")
mat_tela.use_nodes = True
mat_tela.node_tree.nodes["Principio de Diffuso"].inputs[0].default_value = (1, 1, 1, 1)
bpy.context.active_object.data.materials.append(mat_tela)

# Guarda el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])