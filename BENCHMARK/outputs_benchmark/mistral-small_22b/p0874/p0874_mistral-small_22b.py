import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
sofa = bpy.context.object
sofa.name = "Sofa"

# Escalar el sofá para que sea un sofá de tres plazas
bpy.ops.transform.resize(value=(3, 1, 1))

# Cambiar el color del sofá a gris
sofa_material = bpy.data.materials.new(name="GrayMaterial")
sofa_material.diffuse_color = (0.5, 0.5, 0.5)
sofa.data.materials.append(sofa_material)

# Crear la mesa de centro
bpy.ops.mesh.primitive_cube_add(size=1, location=(2, 0, 0))
table = bpy.context.object
table.name = "Table"

# Escalar la mesa para que sea una mesa de centro
bpy.ops.transform.resize(value=(1, 0.5, 1))

# Cambiar el color de la mesa a madera de nogal
table_material = bpy.data.materials.new(name="WoodMaterial")
table_material.diffuse_color = (0.8, 0.4, 0)
table.data.materials.append(table_material)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])