import bpy

# Crear una nueva escena
bpy.ops.scene.new(name="Rascacielos")

# Definir las dimensiones del edificio
altura = 30
ancho_planta = 24
alto_planta = ancho_planta
columnas_x = 10
columnas_y = 10
espacio_columna = 3
altura_columna = altura / (columnas_x * columnas_y)
altura_fachada = altura - (columnas_x + 1) * espacio_columna
altura_piso = altura_fachada / (columnas_x * columnas_y)

# Crear el piso inferior
bpy.ops.mesh.primitive_cube_add(size=ancho_planta, location=(0, 0, 0))
bpy.context.object.name = "PisoInferior"

# Crear las columnas
for x in range(columnas_x):
    for y in range(columnas_y):
        bpy.ops.mesh.primitive_cube_add(size=espacio_columna, location=(x * espacio_columna + espacio_columna / 2, y * espacio_columna + espacio_columna / 2, 0))
        bpy.context.object.name = f"Columna_{x}_{y}"

# Crear los pisos
for i in range(altura):
    bpy.ops.mesh.primitive_cube_add(size=ancho_planta, location=(0, 0, i * altura_piso))
    bpy.context.object.name = f"Piso_{i}"

# Crear la fachada de vidrio
for x in range(columnas_x):
    for y in range(columnas_y):
        bpy.ops.mesh.primitive_cube_add(size=espacio_columna, location=(x * espacio_columna + espacio_columna / 2, y * espacio_columna + espacio_columna / 2, altura_fachada / 2))
        bpy.context.object.name = f"Fachada_{x}_{y}"

# Ajustar la escala para que el edificio tenga la altura correcta
bpy.context.object.scale = (altura, altura, altura)

# Ajustar la posición para que el edificio esté centrado
bpy.context.object.location = (0, 0, 0)

# Guardar el archivo
bpy.ops.wm.save_as_mainfile(filepath="rascacielos.blend")