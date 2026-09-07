import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la cama (en metros)
width = 1.8  # Ancho de la cama
length = 2.0  # Largo del colchón
height = 0.5  # Altura del marco de la cama
colchon_thickness = 0.15 #Grosor del colchón
frame_thickness = 0.05 #Grosor del marco

# Materiales
material_roble = bpy.data.materials.new(name="Roble")
material_roble.use_nodes = True
principled_bsdf = material_roble.node_tree.nodes["Principled BSDF"]
principled_bsdf.inputs["Base Color"].default_value = (0.6, 0.4, 0.2, 1)  # Color roble
principled_bsdf.inputs["Roughness"].default_value = 0.5

material_colchon = bpy.data.materials.new(name="Colchon")
material_colchon.use_nodes = True
principled_bsdf_colchon = material_colchon.node_tree.nodes["Principled BSDF"]
principled_bsdf_colchon.inputs["Base Color"].default_value = (1, 1, 1, 1)  # Blanco
principled_bsdf_colchon.inputs["Roughness"].default_value = 0.8

# Crear el marco de la cama
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, height/2), scale=(width, length, height))
marco_cama = bpy.context.object
marco_cama.name = "MarcoCama"
marco_cama.data.materials.append(material_roble)

# Crear el colchón
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, height + colchon_thickness/2), scale=(width, length, colchon_thickness))
colchon = bpy.context.object
colchon.name = "Colchon"
colchon.data.materials.append(material_colchon)

# Crear patas de la cama
patas_diametro = 0.1
patas_altura = height
patas_x_offset = width/2 - patas_diametro/2
patas_z_offset = 0

# Patas delanteras
bpy.ops.mesh.primitive_cylinder_add(radius=patas_diametro/2, depth=patas_altura, enter_editmode=False, align='WORLD', location=(patas_x_offset, length/2 + patas_diametro/2, patas_altura/2), scale=(1, 1, 1))
pata_delantera_izq = bpy.context.object
pata_delantera_izq.name = "PataDelanteraIzq"
pata_delantera_izq.data.materials.append(material_roble)

bpy.ops.mesh.primitive_cylinder_add(radius=patas_diametro/2, depth=patas_altura, enter_editmode=False, align='WORLD', location=(-patas_x_offset, length/2 + patas_diametro/2, patas_altura/2), scale=(1, 1, 1))
pata_delantera_der = bpy.context.object
pata_delantera_der.name = "PataDelanteraDer"
pata_delantera_der.data.materials.append(material_roble)

# Patas traseras
bpy.ops.mesh.primitive_cylinder_add(radius=patas_diametro/2, depth=patas_altura, enter_editmode=False, align='WORLD', location=(patas_x_offset, -length/2 - patas_diametro/2, patas_altura/2), scale=(1, 1, 1))
pata_trasera_izq = bpy.context.object
pata_trasera_izq.name = "PataTraseraIzq"
pata_trasera_izq.data.materials.append(material_roble)

bpy.ops.mesh.primitive_cylinder_add(radius=patas_diametro/2, depth=patas_altura, enter_editmode=False, align='WORLD', location=(-patas_x_offset, -length/2 - patas_diametro/2, patas_altura/2), scale=(1, 1, 1))
pata_trasera_der = bpy.context.object
pata_trasera_der.name = "PataTraseraDer"
pata_trasera_der.data.materials.append(material_roble)


# Guardar la escena
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])