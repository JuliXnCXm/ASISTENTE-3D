import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la cama (en metros)
ancho_cama = 1.6
largo_cama = 2.0
altura_cama = 0.5  # Altura de la estructura de la cama

# Dimensiones del colchón (ligeramente más pequeño que la cama)
ancho_colchon = ancho_cama - 0.02
largo_colchon = largo_cama - 0.02
grosor_colchon = 0.15

# Materiales
material_nogal = bpy.data.materials.new(name="Nogal")
material_nogal.use_nodes = True
principled_bsdf = material_nogal.node_tree.nodes["Principled BSDF"]
principled_bsdf.inputs["Base Color"].default_value = (0.35, 0.2, 0.1, 1)  # Color marrón nogal
principled_bsdf.inputs["Roughness"].default_value = 0.5

material_blanco = bpy.data.materials.new(name="Blanco")
material_blanco.use_nodes = True
principled_bsdf_blanco = material_blanco.node_tree.nodes["Principled BSDF"]
principled_bsdf_blanco.inputs["Base Color"].default_value = (1, 1, 1, 1)  # Blanco
principled_bsdf_blanco.inputs["Roughness"].default_value = 0.3


# Estructura de la cama (Nogal)
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, altura_cama/2), scale=(ancho_cama/2, largo_cama/2, altura_cama/2))
estructura_cama = bpy.context.object
estructura_cama.name = "Estructura_Cama"
estructura_cama.data.materials.append(material_nogal)

# Colchón (Blanco)
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, altura_cama + grosor_colchon/2), scale=(ancho_colchon/2, largo_colchon/2, grosor_colchon/2))
colchon = bpy.context.object
colchon.name = "Colchon"
colchon.data.materials.append(material_blanco)


# Guardar el archivo .blend si la variable de entorno BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])