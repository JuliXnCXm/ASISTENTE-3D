import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la cama (en metros)
ancho_cama = 1.6
largo_cama = 2.0
altura_estructura = 0.4
grosor_estructura = 0.05

# Materiales
material_roble = bpy.data.materials.new(name="Roble")
material_roble.use_nodes = True
principled_roble = material_roble.node_tree.nodes["Principled BSDF"]
principled_roble.inputs["Base Color"].default_value = (0.6, 0.4, 0.2, 1)  # Color roble
principled_roble.inputs["Roughness"].default_value = 0.5

material_colchon = bpy.data.materials.new(name="Colchon")
material_colchon.use_nodes = True
principled_colchon = material_colchon.node_tree.nodes["Principled BSDF"]
principled_colchon.inputs["Base Color"].default_value = (1, 1, 1, 1)  # Blanco
principled_colchon.inputs["Roughness"].default_value = 0.8

# Estructura de madera (roble)
# Laterales
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, altura_estructura/2), scale=(ancho_cama/2, grosor_estructura, altura_estructura))
lateral_izquierdo = bpy.context.object
lateral_izquierdo.data.materials.append(material_roble)

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(ancho_cama/2, 0, altura_estructura/2), scale=(grosor_estructura, ancho_cama/2, altura_estructura))
lateral_derecho = bpy.context.object
lateral_derecho.data.materials.append(material_roble)

# Cabecera
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(ancho_cama/2, 0, altura_estructura), scale=(ancho_cama, grosor_estructura, 0.1))
cabecera = bpy.context.object
cabecera.data.materials.append(material_roble)

# Base del colchón (textil blanco)
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0.1), scale=(ancho_cama, largo_cama, grosor_estructura))
colchon = bpy.context.object
colchon.data.materials.append(material_colchon)

# Unir la estructura de madera
bpy.ops.object.select_all(action='DESELECT')
lateral_izquierdo.select_set(True)
lateral_derecho.select_set(True)
cabecera.select_set(True)
bpy.ops.object.join()
estructura_cama = bpy.context.object

# Ajustar el origen de la estructura
bpy.ops.object.origin_set(type='ORIGIN_CENTER', center='BOUNDS')

# Guardar el archivo .blend si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])