import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones del edificio
pisos = 5
ancho = 15
largo = 20

# Crear el piso de acceso
plaza = bpy.ops.mesh.primitive_cube_add(location=(0, 0, -1))
bpy.context.object.scale = (largo, ancho, 0.1)

# Crear los pisos del edificio
for i in range(pisos):
    floor = bpy.ops.mesh.primitive_cube_add(location=(0, 0, i + 1))
    bpy.context.object.scale = (largo, ancho, 0.1)
    
    # Crear columnas estructurales
    for j in range(4):  # Suponiendo 4 columnas por piso
        column = bpy.ops.mesh.primitive_cylinder_add(location=(j * largo / 4 - largo / 8, ancho / 2 - ancho / 8, i + 1))
        bpy.context.object.scale = (0.5, 0.5, 3)

# Crear la fachada de cristal
glass幕墙 = bpy.ops.mesh.primitive_cube_add(location=(largo / 2, ancho / 2, pisos + 0.5))
bpy.context.object.scale = (largo, ancho, 1)
bpy.ops.object.shade_smooth()

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    blend_out_path = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)