import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones en metros
pavimento_size = 50
banco_length = 2
banco_width = 1
farola_height = 3
tree_height = 6

# Crear el pavimento de adoquines
for i in range(-pavimento_size, pavimento_size + 1):
    for j in range(-pavimento_size, pavimento_size + 1):
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=(i * 1, j * 1, 0))

# Crear las bancas
for i in range(-pavimento_size // 2, pavimento_size // 2 + 1):
    for j in range(-pavimento_size // 4, pavimento_size // 4 + 1):
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=(i * 2 - 0.5, j * 2 - 0.5, 0))

# Crear las farolas
for i in range(-pavimento_size // 3, pavimento_size // 3 + 1):
    for j in range(-pavimento_size // 6, pavimento_size // 6 + 1):
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=(i * 3 - 0.5, j * 3 - 0.5, farola_height))

# Crear los árboles
for i in range(-pavimento_size // 4, pavimento_size // 4 + 1):
    for j in range(-pavimento_size // 8, pavimento_size // 8 + 1):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(i * 4 - 2, j * 4 - 2, tree_height))

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)