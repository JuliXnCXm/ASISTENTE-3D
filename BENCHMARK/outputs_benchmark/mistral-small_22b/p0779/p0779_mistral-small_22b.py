import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea el sofá
def create_sofa():
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    sofa = bpy.context.object
    sofa.name = "Sofa"
    sofa.scale = (3, 1, 1)

    # Añade material gris
    mat = bpy.data.materials.new(name="GrayMaterial")
    mat.diffuse_color = (0.5, 0.5, 0.5, 1)
    sofa.data.materials.append(mat)

create_sofa()

# Crea la mesa de centro
def create_table():
    bpy.ops.mesh.primitive_cube_add(size=0.2, location=(1.5, 0, -0.5))
    table = bpy.context.object
    table.name = "Table"
    table.scale = (1.5, 0.2, 1.5)

    # Añade material de madera de nogal
    mat = bpy.data.materials.new(name="WoodMaterial")
    mat.diffuse_color = (0.6, 0.3, 0.1, 1)
    table.data.materials.append(mat)

create_table()

# Guarda el archivo .blend si BLEND_OUT está definido
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])