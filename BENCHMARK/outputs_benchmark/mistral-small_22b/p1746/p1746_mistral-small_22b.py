import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Función para crear un cubo
def create_cube(name, size):
    bpy.ops.mesh.primitive_cube_add(size=size, location=(0, 0, 0))
    obj = bpy.context.object
    obj.name = name
    return obj

# Función para crear una columna
def create_column(name, size):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=size, location=(0, 0, 0))
    obj = bpy.context.object
    obj.name = name
    return obj

# Crear base de asfalto
base = create_cube("Base", 2)
bpy.ops.transform.resize(value=(40, 40, 0.1))

# Crear edificio de oficinas
for i in range(5):
    floor = create_cube(f"Floor_{i}", 2)
    bpy.ops.transform.translate(value=(0, 0, i * 4))
    bpy.ops.transform.resize(value=(38, 38, 1))

# Crear columnas visibles
for x in range(-5, 6):
    for z in range(-5, 6):
        create_column(f"Column_{x}_{z}", 4)
        bpy.ops.transform.translate(value=(x * 2, 0, z * 2))

# Crear ventanas en la fachada principal
for y in range(1, 6):
    for x in range(-5, 6):
        create_cube(f"Window_{y}_{x}", 0.1)
        bpy.ops.transform.translate(value=(x * 2, 0, y * 4))

# Guardar el archivo si BLEND_OUT está definido
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])