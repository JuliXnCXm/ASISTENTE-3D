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
sofa.data.polygons.foreach_set("material_index", 0) # Asegurar que tenga un material

# Crear el material del sofá (gris)
material_sofa = bpy.data.materials.new(name="SofaMaterial")
material_sofa.use_nodes = True
bsdf = material_sofa.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.6, 0.6, 0.6, 1)  # Gris
sofa.data.materials.append(material_sofa)


# Crear la mesa de centro
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0.8, 0, table_height/2), scale=(table_width, table_depth, table_height))
table = bpy.context.object
table.name = "CoffeeTable"
bpy.ops.object.shade_smooth()
table.data.polygons.foreach_set("material_index", 0)

# Crear el material de la mesa (nogal)
material_table = bpy.data.materials.new(name="TableMaterial")
material_table.use_nodes = True
bsdf_table = material_table.node_tree.nodes["Principled BSDF"]
bsdf_table.inputs["Base Color"].default_value = (0.4, 0.2, 0.1, 1)  # Nogal
bsdf_table.inputs["Roughness"].default_value = 0.5
table.data.materials.append(material_table)


# Posicionar la mesa frente al sofá
#table.location.x = sofa_width/2 + 0.2
#table.location.y = 0
#table.location.z = table_height/2

# Ajustar la vista
bpy.context.scene.view_layers[0].use_pass_direct = True
bpy.context.scene.camera.location = (5, -5, 2)
bpy.context.scene.camera.rotation_euler = (1.1, 0, 0)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)