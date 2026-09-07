import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la cama (en metros)
width = 1.8  # Ancho de la cama
length = 2.0  # Largo de la cama
height = 0.5  # Altura del marco
thickness = 0.05  # Grosor de la madera

# Dimensiones del colchón (en metros)
mattress_width = width
mattress_length = length
mattress_height = 0.25

# Crear el marco de la cama (roble)
def create_frame(name, width, length, height, thickness, color_name):
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    frame = bpy.context.object
    frame.name = name
    frame.scale = (width/2, length/2, height/2)
    frame.location = (0, 0, height/2)

    # Crear material de roble
    material = bpy.data.materials.new(name=color_name)
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.6, 0.4, 0.2, 1)  # Color roble
    bsdf.inputs["Roughness"].default_value = 0.5
    frame.data.materials.append(material)
    return frame

frame = create_frame("Bed Frame", width, length, height, thickness, "Oak")

# Crear el colchón (blanco)
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
mattress = bpy.context.object
mattress.name = "Mattress"
mattress.scale = (mattress_width/2, mattress_length/2, mattress_height/2)
mattress.location = (0, 0, height)

# Crear material blanco para el colchón
mattress_material = bpy.data.materials.new(name="White Mattress")
mattress_material.use_nodes = True
bsdf_mattress = mattress_material.node_tree.nodes["Principled BSDF"]
bsdf_mattress.inputs["Base Color"].default_value = (1, 1, 1, 1)  # Blanco
bsdf_mattress.inputs["Roughness"].default_value = 0.7
mattress.data.materials.append(mattress_material)


# Guardar el archivo .blend si la variable de entorno BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)