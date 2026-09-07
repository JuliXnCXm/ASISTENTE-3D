import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la cama
ancho = 1.8  # metros
alto = 0.6   # metros
profundidad = 2.0  # metros

# Crea el marco superior de madera de roble
bpy.ops.mesh.primitive_cube_add(location=(0, 0, alto + 0.01))
obj_marco_superior = bpy.context.active_object
obj_marco_superior.scale = (ancho, profundidad, 0.1)
obj_marco_superior.name = 'Marco Superior'

# Crea el marco inferior de madera de roble
bpy.ops.mesh.primitive_cube_add(location=(0, 0, -alto))
obj_marco_inferior = bpy.context.active_object
obj_marco_inferior.scale = (ancho, profundidad, 0.1)
obj_marco_inferior.name = 'Marco Inferior'

# Crea los laterales de madera de roble
bpy.ops.mesh.primitive_cube_add(location=(ancho / 2, 0, alto + 0.01))
obj_lateral_derecha = bpy.context.active_object
obj_lateral_derecha.scale = (0.1, profundidad, alto - 0.02)
obj_lateral_derecha.name = 'Lateral Derecha'

bpy.ops.mesh.primitive_cube_add(location=(-ancho / 2, 0, alto + 0.01))
obj_lateral_izquierda = bpy.context.active_object
obj_lateral_izquierda.scale = (0.1, profundidad, alto - 0.02)
obj_lateral_izquierda.name = 'Lateral Izquierda'

# Crea el colchón blanco
bpy.ops.mesh.primitive_cube_add(location=(0, 0, alto))
obj_colchon = bpy.context.active_object
obj_colchon.scale = (ancho, profundidad, 0.2)
obj_colchon.name = 'Colchon'

# Aplica materiales a los objetos
mat_roble = bpy.data.materials['Material.001']
mat_roble.use_nodes = True

mat_blanco = bpy.data.materials.new(name='Blanco')
mat_blanco.use_nodes = True

bpy.context.collection.objects.link(obj_marco_superior)
bpy.context.collection.objects.link(obj_marco_inferior)
bpy.context.collection.objects.link(obj_lateral_derecha)
bpy.context.collection.objects.link(obj_lateral_izquierda)
bpy.context.collection.objects.link(obj_colchon)

obj_marco_superior.data.materials[0] = mat_roble
obj_marco_inferior.data.materials[0] = mat_roble
obj_lateral_derecha.data.materials[0] = mat_roble
obj_lateral_izquierda.data.materials[0] = mat_roble

obj_colchon.data.materials[0] = mat_blanco

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])