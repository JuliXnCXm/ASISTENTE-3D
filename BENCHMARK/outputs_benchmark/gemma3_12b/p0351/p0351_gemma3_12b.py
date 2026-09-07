import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la cama doble (en metros)
width = 1.6
length = 2.0
height = 0.5  # Altura del marco
mattress_thickness = 0.15
leg_height = 0.3
leg_width = 0.05

# Dimensiones de la estructura de madera de nogal
wood_color = (0.4, 0.2, 0.1, 1)  # Nogal

# Crear las patas de la cama
def create_leg(x, y):
    bpy.ops.mesh.primitive_cube_add(size=leg_width, location=(x, y, leg_height / 2))
    leg = bpy.context.object
    leg.scale = (1, 1, leg_height / leg_width)
    leg.name = "Leg"
    leg.data.materials.append(bpy.data.materials.new(name="Wood"))
    leg.data.materials[0].use_nodes = True
    bsdf = leg.data.materials[0].node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = wood_color
    return leg

leg1 = create_leg(width / 2 - leg_width / 2, length / 2 - leg_width / 2)
leg2 = create_leg(width / 2 - leg_width / 2, -length / 2 + leg_width / 2)
leg3 = create_leg(-width / 2 + leg_width / 2, length / 2 - leg_width / 2)
leg4 = create_leg(-width / 2 + leg_width / 2, -length / 2 + leg_width / 2)


# Crear el marco de la cama
bpy.ops.mesh.primitive_cube_add(size=width, location=(0, 0, height / 2))
frame = bpy.context.object
frame.scale = (1, length / width, height / width)
frame.name = "Frame"
frame.data.materials.append(bpy.data.materials.new(name="Wood"))
frame.data.materials[0].use_nodes = True
bsdf = frame.data.materials[0].node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = wood_color

# Crear el colchón
bpy.ops.mesh.primitive_cube_add(size=width, location=(0, 0, height + mattress_thickness / 2))
mattress = bpy.context.object
mattress.scale = (1, length / width, mattress_thickness / width)
mattress.name = "Mattress"
mattress.data.materials.append(bpy.data.materials.new(name="Fabric"))
mattress.data.materials[0].use_nodes = True
bsdf = mattress.data.materials[0].node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (1, 1, 1, 1)  # Blanco
bsdf.inputs["Roughness"].default_value = 0.6

# Agrupar los objetos
bed_group = bpy.data.objects.new("Bed", None)
for obj in [leg1, leg2, leg3, leg4, frame, mattress]:
    obj.parent = bed_group

# Mover el grupo de la cama al origen
bed_group.location = (0, 0, 0)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])