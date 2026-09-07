import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones del dormitorio en metros
width = 4.0
depth = 3.5
height = 2.5

# Material gris para las paredes
gray_material = bpy.data.materials.new(name="GrayWallMaterial")
gray_material.use_nodes = True
bsdf = gray_material.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1)  # Gris

# Crear paredes
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, height/2), scale=(width, 0.1, depth))
wall_back = bpy.context.object
wall_back.data.materials.append(gray_material)

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, depth/2, height/2), scale=(0.1, depth, height))
wall_right = bpy.context.object
wall_right.data.materials.append(gray_material)

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(width/2, 0, height/2), scale=(width, 0.1, height))
wall_left = bpy.context.object
wall_left.data.materials.append(gray_material)

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, width/2, height/2), scale=(0.1, width, height))
wall_front = bpy.context.object
wall_front.data.materials.append(gray_material)


# Crear cama doble
bed_width = 1.6
bed_depth = 2.0
bed_height = 0.5

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(width/2, -bed_depth/2, bed_height/2), scale=(bed_width, 0.1, bed_depth))
bed_base = bpy.context.object
bed_base.data.materials.append(gray_material) # Usar el mismo material que las paredes para simplificar

# Crear estructura de madera de la cama
wood_material = bpy.data.materials.new(name="WoodMaterial")
wood_material.use_nodes = True
bsdf_wood = wood_material.node_tree.nodes["Principled BSDF"]
bsdf_wood.inputs["Base Color"].default_value = (0.8, 0.6, 0.4, 1)  # Madera

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(width/2, -bed_depth/2, bed_height), scale=(bed_width, 0.05, bed_depth))
bed_frame_back = bpy.context.object
bed_frame_back.data.materials.append(wood_material)

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(width/2, -bed_depth/2 + bed_depth/2, bed_height), scale=(bed_width, 0.05, 0.1))
bed_frame_side = bpy.context.object
bed_frame_side.data.materials.append(wood_material)

# Guardar el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])