import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá
def create_sofa():
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    sofa = bpy.context.object
    sofa.name = "Sofa"

    # Añadir modificador de subdivisión para suavizar la forma
    bpy.ops.object.modifier_add(type='SUBSURF')
    sofa.modifiers["Subsurf"].levels = 2
    sofa.modifiers["Subsurf"].render_levels = 2

    # Cambiar el color a gris
    bpy.ops.object.shade_smooth()
    sofa.data.materials.append(bpy.data.materials.new(name="GrayMaterial"))
    sofa.data.materials[0].diffuse_color = (0.5, 0.5, 0.5, 1)

    # Escalar el sofá para que sea más grande
    bpy.ops.transform.resize(value=(2, 1, 1))

# Crear la mesa de centro
def create_table():
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, -1, 0))
    table = bpy.context.object
    table.name = "Table"

    # Añadir modificador de subdivisión para suavizar la forma
    bpy.ops.object.modifier_add(type='SUBSURF')
    table.modifiers["Subsurf"].levels = 2
    table.modifiers["Subsurf"].render_levels = 2

    # Cambiar el color a marrón oscuro para simular madera de nogal
    bpy.ops.object.shade_smooth()
    table.data.materials.append(bpy.data.materials.new(name="BrownMaterial"))
    table.data.materials[0].diffuse_color = (0.4, 0.2, 0.1, 1)

# Crear el sofá y la mesa de centro
create_sofa()
create_table()

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])