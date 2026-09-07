import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Función para crear adoquines
def create_cobblestone():
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
    obj = bpy.context.object
    obj.scale.x = 0.5
    obj.scale.y = 0.2
    obj.scale.z = 0.01
    obj.name = "Cobblestone"

# Función para crear una banca
def create_bench():
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    obj = bpy.context.object
    obj.scale.x = 2
    obj.scale.y = 0.5
    obj.scale.z = 0.5
    obj.name = "Bench"

# Función para crear una farola
def create_lamp():
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=3, location=(0, 0, 0))
    obj = bpy.context.object
    obj.scale.x = 0.2
    obj.scale.y = 0.2
    obj.scale.z = 4
    obj.name = "Lamp"

# Función para crear un árbol en alcorque cuadrado
def create_tree():
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=2, location=(0, 0, 0))
    obj = bpy.context.object
    obj.scale.x = 0.5
    obj.scale.y = 0.5
    obj.scale.z = 4
    obj.name = "Tree"

# Crear adoquines en una cuadrícula
for x in range(-10, 10):
    for y in range(-10, 10):
        create_cobblestone()
        bpy.context.object.location.x = x
        bpy.context.object.location.y = y

# Crear bancas
for i in range(5):
    for j in range(3):
        create_bench()
        bpy.context.object.location.x = i * 2 - 8
        bpy.context.object.location.y = j * 1.5 - 4.5

# Crear farolas
for i in range(5):
    for j in range(3):
        create_lamp()
        bpy.context.object.location.x = i * 2 - 8
        bpy.context.object.location.y = j * 1.5 - 4.5
        bpy.context.object.location.z = 3

# Crear árboles
for i in range(2):
    for j in range(2):
        create_tree()
        bpy.context.object.location.x = i * 4 - 6
        bpy.context.object.location.y = j * 4 - 6
        bpy.context.object.location.z = 0.5

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])