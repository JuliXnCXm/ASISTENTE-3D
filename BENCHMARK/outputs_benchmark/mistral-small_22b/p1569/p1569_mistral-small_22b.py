import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el edificio
def create_building():
    # Dimensiones del edificio
    width = 15
    depth = 12
    height = 4 * 3  # 4 pisos, cada piso es 3m de alto

    # Crear la base del edificio
    bpy.ops.mesh.primitive_cube_add(size=width, location=(0, 0, -height / 2))
    building = bpy.context.object

    # Añadir columnas
    for x in range(0, width, 3):
        for z in range(0, depth, 3):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.5, height=height, location=(x, 0, z))

    # Añadir ventanas en todas las fachadas
    for x in range(0, width, 3):
        for y in range(1, height - 1, 3):
            bpy.ops.mesh.primitive_plane_add(size=2, location=(x, y, 0))
            bpy.ops.mesh.primitive_plane_add(size=2, location=(x, y, depth))
            bpy.ops.mesh.primitive_plane_add(size=2, location=(0, y, z))
            bpy.ops.mesh.primitive_plane_add(size=2, location=(width, y, z))

# Ejecutar la función para crear el edificio
create_building()

# Guardar el archivo si existe BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])