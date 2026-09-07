import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones y propiedades del edificio
building_width = 20.0  # Ancho en metros
floors = 5             # Número de pisos
window_size = (3.0, 2.0)  # Tamaño de cada ventana en metros

# Crear los pisos
for floor in range(floors):
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, -floor * 4))
    floor_obj = bpy.context.object
    floor_obj.scale = (building_width, building_width, 4.0)

# Crear las ventanas
for x in range(int(building_width / window_size[0])):
    for y in range(int(building_width / window_size[1])):
        for floor in range(floors):
            bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(x * window_size[0] - building_width / 2 + window_size[0] / 2, y * window_size[1] - building_width / 2 + window_size[1] / 2, -floor * 4 + 3))
            window_obj = bpy.context.object
            window_obj.scale = (window_size[0], window_size[1], 1.0)

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)