import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá
def create_sofa():
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    sofa = bpy.context.object
    sofa.name = "Sofa"

    # Añadir material gris
    mat = bpy.data.materials.new(name="GrayMaterial")
    mat.diffuse_color = (0.5, 0.5, 0.5)
    sofa.data.materials.append(mat)

    # Escalar el sofá para que sea de 3 plazas
    bpy.ops.object.transform_apply(scale=True)
    sofa.scale = (2, 1, 0.5)

# Crear la mesa de centro
def create_table():
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    table = bpy.context.object
    table.name = "Table"

    # Añadir material de madera de nogal
    mat = bpy.data.materials.new(name="WoodMaterial")
    mat.diffuse_color = (0.5, 0.3, 0.1)
    table.data.materials.append(mat)

    # Escalar la mesa para que tenga un tamaño adecuado
    bpy.ops.object.transform_apply(scale=True)
    table.scale = (1, 0.5, 0.2)

# Crear el sofá y la mesa de centro
create_sofa()
create_table()

# Guardar el archivo .blend si existe BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])