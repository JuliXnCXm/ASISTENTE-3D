import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la cama (en metros)
width = 1.60
length = 2.00
height = 0.50  # Altura de la estructura de la cama
thickness = 0.05 # Grosor de la madera

# Materiales
oak_material = bpy.data.materials.new(name="OakWood")
oak_material.use_nodes = True
bsdf = oak_material.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.6, 0.4, 0.2, 1)  # Color roble
bsdf.inputs["Roughness"].default_value = 0.5
bsdf.inputs["Metallic"].default_value = 0.0

white_material = bpy.data.materials.new(name="WhiteFabric")
white_material.use_nodes = True
bsdf_white = white_material.node_tree.nodes["Principled BSDF"]
bsdf_white.inputs["Base Color"].default_value = (1, 1, 1, 1)  # Blanco
bsdf_white.inputs["Roughness"].default_value = 0.8
bsdf_white.inputs["Specular"].default_value = 0.1


# Estructura de la cama (roble)
def create_frame(name, width, length, height, thickness, material):
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    frame = bpy.context.object
    frame.name = name
    frame.scale = (width/2, length/2, height/2)
    frame.location = (0, 0, height/2)
    frame.data.materials.append(material)
    return frame

# Crear las partes de la estructura
base = create_frame("Base", width, length, thickness, thickness, oak_material)
side1 = create_frame("Side1", thickness, height, width, thickness, oak_material)
side1.rotation_euler[0] = 1.5708  # 90 grados en radianes
side1.location = (width/2 + thickness/2, 0, height/2)

side2 = create_frame("Side2", thickness, height, width, thickness, oak_material)
side2.rotation_euler[0] = 1.5708
side2.location = (-width/2 - thickness/2, 0, height/2)

headboard = create_frame("Headboard", width, thickness, height, thickness, oak_material)
headboard.location = (0, length/2 + thickness/2, height/2)

footboard = create_frame("Footboard", width, thickness, height, thickness, oak_material)
footboard.location = (0, -length/2 - thickness/2, height/2)

# Colchón (blanco)
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
mattress = bpy.context.object
mattress.name = "Mattress"
mattress.scale = (width/2, length/2, 0.2)
mattress.location = (0, 0, 0.2)
mattress.data.materials.append(white_material)


# Opcional: Guardar el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])