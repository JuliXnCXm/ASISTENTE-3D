import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el edificio
def create_building():
    # Dimensiones del edificio
    width = 15
    depth = 20
    height = 5 * 4  # 5 pisos de 4 metros cada uno

    # Crear la base del edificio
    bpy.ops.mesh.primitive_cube_add(size=width, location=(0, 0, -height / 2))
    building = bpy.context.object
    building.name = "Building"

    # Crear las columnas estructurales
    for x in range(-width // 4, width // 4 + 1):
        for z in range(-depth // 4, depth // 4 + 1):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=height, location=(x * 4, 0, z * 4))
            column = bpy.context.object
            column.name = f"Column_{x}_{z}"

    # Crear la plaza de acceso
    bpy.ops.mesh.primitive_plane_add(size=25, location=(0, -depth / 2, -height / 2))
    plaza = bpy.context.object
    plaza.name = "Plaza"

    # Crear la fachada de cristal
    for x in range(-width // 4, width // 4 + 1):
        for z in range(-depth // 4, depth // 4 + 1):
            bpy.ops.mesh.primitive_plane_add(size=4, location=(x * 4, -height / 2, z * 4))
            glass = bpy.context.object
            glass.name = f"Glass_{x}_{z}"

# Ejecutar la función para crear el edificio
create_building()

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])