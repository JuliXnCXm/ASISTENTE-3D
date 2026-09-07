import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir dimensiones del edificio
pisos = 4
ancho = 15
largo = 12

# Crear columnas y estructura
for piso in range(pisos):
    for x in range(0, ancho * 3 + 1, 3):  # 3 metros entre columnas
        bpy.ops.mesh.primitive_cube_add(location=(x - (ancho * 1.5), -largo / 2, piso * 3))
    for y in range(0, largo * 3 + 1, 3):
        bpy.ops.mesh.primitive_cube_add(location=(-ancho / 2, y - (largo * 1.5), piso * 3))

# Crear paredes
for x in range(-ancho / 2, ancho / 2 + 0.5, 3):
    for z in range(0, pisos * 3 + 1, 3):
        bpy.ops.mesh.primitive_cube_add(location=(x, -largo / 2 - 0.5, z))
for y in range(-largo / 2, largo / 2 + 0.5, 3):
    for z in range(0, pisos * 3 + 1, 3):
        bpy.ops.mesh.primitive_cube_add(location=(-ancho / 2 - 0.5, y, z))

# Crear ventanas
for x in range(-ancho / 2 + 1.5, ancho / 2 - 1.5, 6):  # 3 metros entre columnas
    for y in range(-largo / 2 + 1.5, largo / 2 - 1.5, 6):
        for piso in range(0, pisos * 3, 3):
            bpy.ops.mesh.primitive_cube_add(location=(x, y, piso), scale=(1, 1, 3))

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    blend_out = os.environ['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out)