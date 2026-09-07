import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Parámetros del edificio
ancho = 20
fondo = 15
altura = 5 * 3  # 3 metros por piso
columna_espaciado = 4
ventana_ancho = 1.5
ventana_alto = 2

# Crear el edificio
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, ancho / 2, fondo / 2))
edificio = bpy.context.object

# Ajustar dimensiones del edificio
edificio.scale = (ancho / 2, altura / 2, fondo / 2)

# Crear columnas estructurales
for i in range(0, ancho + columna_espaciado, columna_espaciado):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=altura, location=(i, 0, fondo / 2))

# Crear retícula de ventanas
for i in range(0, ancho + columna_espaciado, columna_espaciado):
    for j in range(0, fondo + columna_espaciado, columna_espaciado):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(i, 0, j))
        ventana = bpy.context.object
        ventana.scale = (ventana_ancho / 2, altura / 2, ventana_alto / 2)

# Guardar el archivo si la variable de entorno BLEND_OUT existe
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])