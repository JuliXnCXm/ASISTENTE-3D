import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las propiedades de la cama
ancho = 1.60
largo = 2.00
alto = 0.20
espesor_madera = 0.05

# Crea el marco superior de madera
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(0, ancho/2, alto))
obj_marco_superior = bpy.context.active_object
obj_marco_superior.name = "Marco Superior"
obj_marco_superior.scale = (ancho, largo, 1)
obj_marco_superior.location = (0, ancho/2, alto)

# Crea el marco inferior de madera
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(0, ancho/2, -alto))
obj_marco_inferior = bpy.context.active_object
obj_marco_inferior.name = "Marco Inferior"
obj_marco_inferior.scale = (ancho, largo, 1)
obj_marco_inferior.location = (0, ancho/2, -alto)

# Crea la estructura de madera entre los marcos superior e inferior
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(0, ancho/2, 0))
obj_estructura_madera = bpy.context.active_object
obj_estructura_madera.name = "Estructura Madera"
obj_estructura_madera.scale = (ancho, largo, alto)
obj_estructura_madera.location = (0, ancho/2, 0)

# Crea el colchón blanco
bpy.ops.mesh.primitive_cube_add(size=1.60, location=(0, 1.00, -alto))
obj_colchon = bpy.context.active_object
obj_colchon.name = "Colchon"
obj_colchon.scale = (ancho, largo, alto)
obj_colchon.location = (0, ancho/2, -alto)

# Aplica materiales a los objetos
mat_madera = bpy.data.materials.new(name="Madera")
mat_madera.diffuse_color = (1.00, 0.50, 0.00) # Color madera de roble

obj_marco_superior.data.materials.append(mat_madera)
obj_marco_inferior.data.materials.append(mat_madera)
obj_estructura_madera.data.materials.append(mat_madera)

mat_colchon = bpy.data.materials.new(name="Colchon")
mat_colchon.diffuse_color = (1.00, 1.00, 1.00) # Color blanco

obj_colchon.data.materials.append(mat_colchon)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in bpy.context.user_preferences.addons['save_load'].preferences.save_path:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.user_preferences.addons['save_load'].preferences.save_path + '/cama_de_matrimonio.blend')