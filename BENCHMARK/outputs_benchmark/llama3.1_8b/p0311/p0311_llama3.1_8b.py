import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las propiedades de la cama
longitud = 2.0  # metros
ancho = 1.5  # metros
alto = 0.8  # metros
espesor_madera = 0.05  # metros

# Crea el marco superior de la cama (estructura de madera)
bpy.ops.mesh.primitive_cube_add(size=longitud, location=(0, 0, alto))
obj_marco_superior = bpy.context.active_object
obj_marco_superior.name = 'Marco Superior'
obj_marco_superior.scale = (ancho, longitud, espesor_madera)

# Crea el marco inferior de la cama (estructura de madera)
bpy.ops.mesh.primitive_cube_add(size=longitud, location=(0, 0, -alto))
obj_marco_inferior = bpy.context.active_object
obj_marco_inferior.name = 'Marco Inferior'
obj_marco_inferior.scale = (ancho, longitud, espesor_madera)

# Crea los laterales de la cama (estructura de madera)
bpy.ops.mesh.primitive_cube_add(size=alto, location=(0, ancho/2, 0))
obj_lateral_derecha = bpy.context.active_object
obj_lateral_derecha.name = 'Lateral Derecha'
obj_lateral_derecha.scale = (ancho, espesor_madera, longitud)

bpy.ops.mesh.primitive_cube_add(size=alto, location=(0, -ancho/2, 0))
obj_lateral_izquierda = bpy.context.active_object
obj_lateral_izquierda.name = 'Lateral Izquierda'
obj_lateral_izquierda.scale = (ancho, espesor_madera, longitud)

# Crea el colchón blanco
bpy.ops.mesh.primitive_plane_add(size=longitud, location=(0, 0, alto - espesor_madera))
obj_colchon = bpy.context.active_object
obj_colchon.name = 'Colchon'
obj_colchon.scale = (ancho, longitud, 0.1)

# Aplica materiales a los objetos
mat_roble = bpy.data.materials['Material.001']
obj_marco_superior.data.materials.append(mat_roble)
obj_marco_inferior.data.materials.append(mat_roble)
obj_lateral_derecha.data.materials.append(mat_roble)
obj_lateral_izquierda.data.materials.append(mat_roble)

mat_blanco = bpy.data.materials['Material.002']
obj_colchon.data.materials.append(mat_blanco)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])