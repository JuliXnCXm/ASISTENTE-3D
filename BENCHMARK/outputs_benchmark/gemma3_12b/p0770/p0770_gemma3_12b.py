import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# --- Funciones de utilidad ---
def create_material(name, color, specular=0.5, roughness=0.5):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    if not bsdf:
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Specular'].default_value = specular
    bsdf.inputs['Roughness'].default_value = roughness
    return mat

# --- Crear materiales ---
gray_fabric_mat = create_material("GrayFabric", (0.6, 0.6, 0.6, 1.0), specular=0.1, roughness=0.8)
wood_mat = create_material("Wood", (0.8, 0.6, 0.4, 1.0), specular=0.3, roughness=0.7)

# --- Crear sofá de tres plazas ---
sofa_width = 2.0
sofa_depth = 0.8
sofa_height = 0.7
back_height = 0.5

# Cuerpo del sofá
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, sofa_height/2), scale=(sofa_width, sofa_depth, 0.1))
sofa_body = bpy.context.object
sofa_body.name = "SofaBody"
sofa_body.data.materials.append(gray_fabric_mat)

# Respaldo del sofá
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, -sofa_depth/2, sofa_height + back_height/2), scale=(sofa_width, 0.1, back_height))
sofa_back = bpy.context.object
sofa_back.name = "SofaBack"
sofa_back.data.materials.append(gray_fabric_mat)

# Brazos del sofá
arm_width = 0.2
arm_depth = sofa_depth
arm_height = sofa_height
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(sofa_width/2 + arm_width/2, 0, arm_height/2), scale=(arm_width, arm_depth, arm_height))
arm_right = bpy.context.object
arm_right.name = "SofaArmRight"
arm_right.data.materials.append(gray_fabric_mat)

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(-sofa_width/2 - arm_width/2, 0, arm_height/2), scale=(arm_width, arm_depth, arm_height))
arm_left = bpy.context.object
arm_left.name = "SofaArmLeft"
arm_left.data.materials.append(gray_fabric_mat)


# --- Crear mesa de centro ---
table_width = 1.2
table_depth = 0.6
table_height = 0.4

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, table_height/2), scale=(table_width, table_depth, table_height))
table = bpy.context.object
table.name = "CoffeeTable"
table.data.materials.append(wood_mat)


# --- Posicionar los objetos ---
sofa_x = 1.0
sofa_y = 1.0
sofa_z = 0.0

table_x = sofa_x
table_y = sofa_y + sofa_depth + 0.2
table_z = sofa_z

sofa_body.location = (sofa_x, sofa_y, sofa_z)
sofa_back.location = (sofa_x, sofa_y, sofa_z)
arm_right.location = (sofa_x, sofa_y, sofa_z)
arm_left.location = (sofa_x, sofa_y, sofa_z)
table.location = (table_x, table_y, table_z)

# --- Guardar la escena ---
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])
else:
    print("No BLEND_OUT environment variable found.  Not saving.")