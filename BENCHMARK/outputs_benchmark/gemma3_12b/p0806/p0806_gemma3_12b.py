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
fabric_gray_mat = create_material("FabricGray", (0.7, 0.7, 0.7, 1.0), specular=0.1, roughness=0.8)
wood_walnut_mat = create_material("WoodWalnut", (0.4, 0.2, 0.1, 1.0), specular=0.3, roughness=0.6)


# --- Crear el sofá ---
sofa_width = 2.0
sofa_depth = 0.8
sofa_height = 0.7
sofa_back_height = 0.5

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, sofa_height/2), scale=(sofa_width, sofa_depth, sofa_height))
sofa_cube = bpy.context.object
sofa_cube.name = "Sofa"
sofa_cube.data.materials.clear()
sofa_cube.data.materials.append(fabric_gray_mat)

# Crear respaldo del sofá
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, sofa_depth/2 + 0.05, sofa_height/2 + sofa_back_height), scale=(sofa_width, 0.05, sofa_back_height))
sofa_back = bpy.context.object
sofa_back.name = "SofaBack"
sofa_back.data.materials.clear()
sofa_back.data.materials.append(fabric_gray_mat)

# --- Crear la mesa de centro ---
table_width = 1.2
table_depth = 0.6
table_height = 0.4

bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, table_height/2), scale=(table_width, table_depth, table_height))
table_cube = bpy.context.object
table_cube.name = "CoffeeTable"
table_cube.data.materials.clear()
table_cube.data.materials.append(wood_walnut_mat)

# --- Posicionar objetos ---
sofa_x = -1.0
sofa_y = 0.0
sofa_z = 0.0

table_x = sofa_x
table_y = sofa_y + sofa_depth + 0.2
table_z = sofa_z

sofa_cube.location = (sofa_x, sofa_y, sofa_z)
sofa_back.location = (sofa_x, sofa_y + sofa_depth + 0.05, sofa_z + sofa_back_height/2)
table_cube.location = (table_x, table_y, table_z)


# --- Guardar el archivo ---
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])