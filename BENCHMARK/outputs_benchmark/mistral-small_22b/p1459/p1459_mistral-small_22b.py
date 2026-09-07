import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Función para crear un cubo
def create_cuboid(location, size):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.scale = (size[0], size[1], size[2])
    return obj

# Crear el edificio de oficinas
width, depth, height = 20, 15, 4
location = (0, 0, 0)

# Crear la base del edificio
base = create_cuboid(location, (width, depth, height))

# Añadir material de hormigón a las fachadas
material_concrete = bpy.data.materials.new(name="Concrete")
material_concrete.diffuse_color = (0.5, 0.5, 0.5)

for face in base.data.polygons:
    if face.normal == (1, 0, 0) or face.normal == (-1, 0, 0):
        face.material_index = 0

# Crear columnas estructurales
column_size = 2
columns = []
for i in range(width // column_size + 1):
    for j in range(depth // column_size + 1):
        col_location = (i * column_size, j * column_size, height / 2)
        col = create_cuboid(col_location, (column_size, column_size, height))
        columns.append(col)

# Añadir material de hormigón a las columnas
for col in columns:
    for face in col.data.polygons:
        if face.normal == (0, 1, 0):
            face.material_index = 0

# Crear ventanas en todas las fachadas
window_size = 2
windows = []
for i in range(width // window_size + 1):
    for j in range(depth // window_size + 1):
        if i == 0 or i == width // window_size or j == 0 or j == depth // window_size:
            win_location = (i * window_size, j * window_size, height / 2)
            win = create_cuboid(win_location, (window_size, window_size, 1))
            windows.append(win)

# Añadir material de ventana a las ventanas
material_window = bpy.data.materials.new(name="Window")
material_window.diffuse_color = (0.8, 0.8, 0.8)

for win in windows:
    for face in win.data.polygons:
        if face.normal == (1, 0, 0) or face.normal == (-1, 0, 0):
            face.material_index = 1

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])