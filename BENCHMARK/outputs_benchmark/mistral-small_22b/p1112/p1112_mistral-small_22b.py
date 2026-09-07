import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá de tela gris de 3 plazas
def create_sofa():
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    sofa = bpy.context.object
    sofa.name = "Sofa"

    # Escalar el sofá para que tenga aproximadamente el tamaño de un sofá de 3 plazas
    sofa.scale = (2, 1, 0.5)

    # Crear material gris
    mat = bpy.data.materials.new(name="GrayMaterial")
    mat.diffuse_color = (0.5, 0.5, 0.5, 1)
    sofa.data.materials.append(mat)

# Crear la mesa de centro de madera de nogal
def create_table():
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(1, 0, -0.25))
    table = bpy.context.object
    table.name = "Table"

    # Escalar la mesa para que tenga aproximadamente el tamaño de una mesa de centro
    table.scale = (1, 0.5, 0.2)

    # Crear material de madera de nogal
    mat = bpy.data.materials.new(name="WoodMaterial")
    mat.diffuse_color = (0.8, 0.4, 0.1, 1)
    table.data.materials.append(mat)

# Crear el sofá y la mesa
create_sofa()
create_table()

# Guardar el archivo .blend si BLEND_OUT está definido
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])