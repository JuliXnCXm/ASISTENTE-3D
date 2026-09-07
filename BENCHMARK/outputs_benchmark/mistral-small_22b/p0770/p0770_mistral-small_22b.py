import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea el sofá de tres plazas
def create_sofa():
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    sofa = bpy.context.object
    sofa.name = "Sofa"

    # Añadir modificador de subdivisión para suavizar el sofá
    bpy.ops.object.modifier_add(type='SUBSURF')
    sofa.modifiers["Subsurf"].levels = 2
    sofa.modifiers["Subsurf"].render_levels = 2

    # Cambiar el color a gris
    sofa.data.materials.append(bpy.data.materials.new(name="GrayMaterial"))
    sofa.data.materials[0].diffuse_color = (0.5, 0.5, 0.5)

create_sofa()

# Crea la mesa de centro
def create_table():
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=0.2, location=(1, 0, 0))
    table = bpy.context.object
    table.name = "Table"

    # Añadir modificador de subdivisión para suavizar la mesa
    bpy.ops.object.modifier_add(type='SUBSURF')
    table.modifiers["Subsurf"].levels = 2
    table.modifiers["Subsurf"].render_levels = 2

    # Cambiar el color a marrón (madera)
    table.data.materials.append(bpy.data.materials.new(name="BrownMaterial"))
    table.data.materials[0].diffuse_color = (0.5, 0.3, 0.1)

create_table()

# Guardar el archivo .blend si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])