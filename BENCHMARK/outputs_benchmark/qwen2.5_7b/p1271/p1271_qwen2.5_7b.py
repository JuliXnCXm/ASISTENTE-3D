import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones del terreno y la casa
terreno_size = (25, 20)
casa_size = (12, 9)

# Crear el terreno de césped
bpy.ops.mesh.primitive_plane_add(size=terreno_size[0], location=(0, 0, -0.1))
terreno = bpy.context.object
terreno.name = "Terreno"

# Crear la casa
bpy.ops.mesh.primitive_cube_add(size=1, location=((terreno_size[0] - casa_size[0]) / 2, (terreno_size[1] - casa_size[1]) / 2, 3))
casa = bpy.context.object
casa.name = "Casa"

# Ajustar la escala de la casa para que tenga las dimensiones correctas
bpy.ops.transform.resize(value=(casa_size[0], casa_size[1], 6))

# Crear el tejado a dos aguas
tejado = bpy.ops.mesh.primitive_cylinder_add(radius=5, depth=2, location=((terreno_size[0] - casa_size[0]) / 4, (terreno_size[1] - casa_size[1]) / 2, 6))
bpy.ops.transform.resize(value=(casa_size[0] / 2.5, casa_size[1] / 2.5, 1))

# Crear el árbol en el jardín frontal
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(-terreno_size[0]/4 + casa_size[0]/2, terreno_size[1]/2 - casa_size[1]/2, 3))
arbol = bpy.context.object
arbol.name = "Arbol"

# Ajustar la escala del árbol para que sea más realista
bpy.ops.transform.resize(value=(0.5, 0.5, 0.5))

# Guardar el archivo .blend si existe BLEND_OUT en las variables de entorno
import os
if "BLEND_OUT" in os.environ:
    blend_out = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out)