import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el edificio de oficinas
def create_building():
    # Dimensiones del edificio
    width = 20
    depth = 15
    height = 4 * 3  # 3 metros por piso
    column_spacing = 3
    window_height = 2
    window_width = 1.5

    # Crear el suelo
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    floor = bpy.context.object
    floor.scale = (width, depth, 0.1)

    # Crear las paredes
    for i in range(4):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, height / 2))
        wall = bpy.context.object
        if i == 0:  # Pared frontal
            wall.scale = (height, depth, width)
            wall.location = (width / 2, 0, height / 2)
        elif i == 1:  # Pared trasera
            wall.scale = (height, depth, width)
            wall.location = (-width / 2, 0, height / 2)
        elif i == 2:  # Pared izquierda
            wall.scale = (height, width, depth)
            wall.location = (0, -depth / 2, height / 2)
        elif i == 3:  # Pared derecha
            wall.scale = (height, width, depth)
            wall.location = (0, depth / 2, height / 2)

    # Crear las columnas estructurales
    for x in range(0, width, column_spacing):
        for z in range(0, depth, column_spacing):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=height, location=(x, 0, z))
            column = bpy.context.object
            column.scale = (1, 1, height / 3)

    # Crear las ventanas en todas las fachadas
    for x in range(0, width, window_width):
        for z in range(0, depth, window_width):
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x + window_width / 2, 0, z + window_height / 2))
            window = bpy.context.object
            window.scale = (window_width, window_height, 0.1)

# Ejecutar la función para crear el edificio
create_building()

# Guardar el archivo .blend si BLEND_OUT está definido
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])