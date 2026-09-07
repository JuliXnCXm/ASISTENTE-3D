import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Parámetros del edificio
ancho = 20
profundidad = 15
altura = 5 * 3  # 3 metros por piso
espacio_ventanas = 1.5  # Espacio entre ventanas

# Crear el suelo
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho / 2, profundidad / 2, 0))
bpy.context.object.scale = (ancho, profundidad, 0.01)

# Crear las paredes
for i in range(4):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, altura / 2))
    bpy.context.object.scale = (altura, espacio_ventanas, ancho if i % 2 == 0 else profundidad)
    bpy.context.object.location = (ancho / 2 if i == 0 else -ancho / 2, profundidad / 2 if i == 1 else -profundidad / 2, altura / 2)

# Crear la fachada de muro cortina simulada por una retícula de ventanas
for x in range(0, ancho, espacio_ventanas):
    for y in range(0, profundidad, espacio_ventanas):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x + espacio_ventanas / 2, y + espacio_ventanas / 2, altura))
        bpy.context.object.scale = (espacio_ventanas, espacio_ventanas, 0.01)

# Guardar el archivo si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])