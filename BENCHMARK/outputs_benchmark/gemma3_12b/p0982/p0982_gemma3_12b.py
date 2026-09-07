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
    sofa_width = 2.0
    sofa_depth = 0.8
    sofa_height = 0.7
    back_height = 0.5

    # Crear el cuerpo principal del sofá
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, sofa_height/2), scale=(sofa_width, sofa_depth, sofa_height))
    sofa_body = bpy.context.object
    sofa_body.name = "Sofa_Body"
    
    # Crear el respaldo del sofá
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, -sofa_depth/2, sofa_height + back_height/2), scale=(sofa_width, 0.1, back_height))
    sofa_back = bpy.context.object
    sofa_back.name = "Sofa_Back"

    # Crear material de cuero
    leather_mat = create_material("Leather", (0.8, 0.6, 0.3, 1.0), 0.4)
    sofa_body.data.materials.append(leather_mat)
    sofa_back.data.materials.append(leather_mat)

# --- Crear la mesa de centro ---
def create_coffee_table():
    # Dimensiones de la mesa (en metros)
    table_width = 1.2
    table_depth = 0.6
    table_height = 0.45

    # Crear la tapa de la mesa
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, table_height/2), scale=(table_width, table_depth, 0.05))
    table_top = bpy.context.object
    table_top.name = "Coffee_Table_Top"

    # Crear las patas de la mesa (4 patas)
    leg_width = 0.1
    leg_height = table_height
    leg_depth = 0.1

    # Patas
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(table_width/2 - leg_width/2, table_depth/2 - leg_depth/2, leg_height/2), scale=(leg_width, leg_depth, leg_height))
    leg1 = bpy.context.object
    leg1.name = "Coffee_Table_Leg_1"

    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(-table_width/2 + leg_width/2, table_depth/2 - leg_depth/2, leg_height/2), scale=(leg_width, leg_depth, leg_height))
    leg2 = bpy.context.object
    leg2.name = "Coffee_Table_Leg_2"

    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(table_width/2 - leg_width/2, -table_depth/2 + leg_depth/2, leg_height/2), scale=(leg_width, leg_depth, leg_height))
    leg3 = bpy.context.object
    leg3.name = "Coffee_Table_Leg_3"

    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(-table_width/2 + leg_width/2, -table_depth/2 + leg_depth/2, leg_height/2), scale=(leg_width, leg_depth, leg_height))
    leg4 = bpy.context.object
    leg4.name = "Coffee_Table_Leg_4"

    # Crear material de madera de nogal
    walnut_mat = create_material("Walnut", (0.4, 0.2, 0.1, 1.0), 0.8)
    table_top.data.materials.append(walnut_mat)
    leg1.data.materials.append(walnut_mat)
    leg2.data.materials.append(walnut_mat)
    leg3.data.materials.append(walnut_mat)
    leg4.data.materials.append(walnut_mat)

# --- Llamar a las funciones para crear los objetos ---
create_sofa()
create_coffee_table()

# --- Guardar la escena (opcional) ---
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])