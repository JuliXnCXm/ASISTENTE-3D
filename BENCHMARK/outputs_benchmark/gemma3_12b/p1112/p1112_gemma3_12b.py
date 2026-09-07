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

# Crear sofá
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, sofa_height/2), scale=(sofa_width, sofa_depth, sofa_height))
sofa = bpy.context.object
sofa.name = "Sofa"

# Subdividir el sofá para dar forma
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=2)
bpy.ops.object.mode_set(mode='OBJECT')

# Modificar la forma del sofá (ejemplo básico)
for vertex in sofa.data.vertices:
    if vertex.co.z > sofa_height * 0.7:
        vertex.co.z -= 0.05

# Crear material para el sofá (tela gris)
sofa_material = bpy.data.materials.new(name="SofaMaterial")
sofa_material.use_nodes = True
bsdf = sofa_material.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1)  # Gris
bsdf.inputs["Roughness"].default_value = 0.7
sofa.data.materials.append(sofa_material)

# Crear mesa de centro
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(1.5, 0, table_height/2), scale=(table_width, table_depth, table_height))
table = bpy.context.object
table.name = "CoffeeTable"

# Crear material para la mesa (madera de nogal)
table_material = bpy.data.materials.new(name="WoodMaterial")
table_material.use_nodes = True
bsdf_table = table_material.node_tree.nodes["Principled BSDF"]
bsdf_table.inputs["Base Color"].default_value = (0.4, 0.2, 0.1, 1)  # Nogal
bsdf_table.inputs["Roughness"].default_value = 0.4
table.data.materials.append(table_material)

# Ajustar la posición de la mesa
table.location.x += 1.5

# Opcional: Guardar el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])