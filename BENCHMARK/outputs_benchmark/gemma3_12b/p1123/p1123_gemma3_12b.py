import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# --- Funciones de utilidad ---
def create_material(name, color, roughness):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    if not bsdf:
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = roughness
    return mat

# --- Crear el sofá ---
def create_sofa():
    # Dimensiones del sofá (en metros)
    width = 2.1  # Ancho
    depth = 0.8  # Profundidad
    height = 0.7  # Altura
    back_height = 0.4 # Altura del respaldo

    # Crear el cuerpo principal del sofá
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, height/2), scale=(width, depth, height))
    sofa_body = bpy.context.object
    sofa_body.name = "Sofa_Body"
    sofa_body.data.name = "Sofa_Body_Mesh"

    # Crear el respaldo
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, -depth/2 + 0.05, height + back_height/2), scale=(width, 0.05, back_height))
    sofa_back = bpy.context.object
    sofa_back.name = "Sofa_Back"
    sofa_back.data.name = "Sofa_Back_Mesh"

    # Crear los brazos del sofá
    arm_width = 0.15
    arm_depth = depth
    arm_height = height
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(width/2 + arm_width/2, 0, arm_height/2), scale=(arm_width, arm_depth, arm_height))
    arm_right = bpy.context.object
    arm_right.name = "Sofa_Arm_Right"
    arm_right.data.name = "Sofa_Arm_Right_Mesh"

    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(-width/2 - arm_width/2, 0, arm_height/2), scale=(arm_width, arm_depth, arm_height))
    arm_left = bpy.context.object
    arm_left.name = "Sofa_Arm_Left"
    arm_left.data.name = "Sofa_Arm_Left_Mesh"

    # Material del sofá (tela gris)
    sofa_material = create_material("Sofa_Fabric", (0.3, 0.3, 0.3, 1), 0.6)
    sofa_body.data.materials.append(sofa_material)
    sofa_back.data.materials.append(sofa_material)
    arm_right.data.materials.append(sofa_material)
    arm_left.data.materials.append(sofa_material)


# --- Crear la mesa de centro ---
def create_coffee_table():
    # Dimensiones de la mesa (en metros)
    width = 1.2
    depth = 0.6
    height = 0.45

    # Crear la mesa
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, height/2), scale=(width, depth, height))
    table = bpy.context.object
    table.name = "Coffee_Table"
    table.data.name = "Coffee_Table_Mesh"

    # Material de la mesa (madera de nogal)
    table_material = create_material("Walnut_Wood", (0.4, 0.2, 0.1, 1), 0.8)
    table.data.materials.append(table_material)

# --- Llamar a las funciones para crear los objetos ---
create_sofa()
create_coffee_table()

# --- Posicionar la mesa frente al sofá ---
sofa_location = sofa_body.location
table_location = (0, -width/2 - 0.1, sofa_location[2])
table = bpy.data.objects["Coffee_Table"]
table.location = table_location

# --- Guardar la escena si la variable de entorno BLEND_OUT está definida ---
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)