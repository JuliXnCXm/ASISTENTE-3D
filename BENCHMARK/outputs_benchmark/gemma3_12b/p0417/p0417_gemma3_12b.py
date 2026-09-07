import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones en metros
sofa_width = 2.4
sofa_depth = 1.0
sofa_height = 0.8
table_width = 1.2
table_depth = 0.6
table_height = 0.45

# Crear el sofá
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, sofa_height/2), scale=(sofa_width, sofa_depth, sofa_height))
sofa = bpy.context.object
sofa.name = "Sofa"
bpy.ops.object.shade_smooth()
sofa_material = bpy.data.materials.new(name="SofaMaterial")
sofa_material.use_nodes = True
bsdf = sofa_material.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)  # Gris claro
bsdf.inputs["Roughness"].default_value = 0.6
sofa.data.materials.append(sofa_material)


# Crear la mesa de centro
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, -table_depth/2, table_height/2), scale=(table_width, table_depth, table_height))
table = bpy.context.object
table.name = "Table"
bpy.ops.object.shade_smooth()
table_material = bpy.data.materials.new(name="TableMaterial")
table_material.use_nodes = True
bsdf_table = table_material.node_tree.nodes["Principled BSDF"]
bsdf_table.inputs["Base Color"].default_value = (0.6, 0.4, 0.2, 1)  # Madera
bsdf_table.inputs["Roughness"].default_value = 0.7
table.data.materials.append(table_material)

# Posicionar los objetos
# El sofá está en (0,0,0)
# La mesa está ligeramente delante del sofá
table.location.x = 0
table.location.y = -1.5
table.location.z = table_height/2

# Guardar el archivo .blend si la variable de entorno BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])