import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones del edificio
pisos = 4
ancho = 20
largo = 15

# Crear el suelo
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -1))
suelo = bpy.context.object
suelo.scale = (ancho, largo, 0.1)

# Crear los pisos superiores
for i in range(1, pisos + 1):
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -1 + i))
    piso = bpy.context.object
    piso.scale = (ancho, largo, 0.1)

# Crear la fachada de hormigón
bpy.ops.mesh.primitive_cube_add(size=5, location=(-20, 7.5, 3))
fachada_hormigon = bpy.context.object
fachada_hormigon.scale = (40, 15, 4)

# Crear las columnas estructurales
for i in range(5):
    for j in range(3):
        columna_x = -20 + 8 * i
        columna_z = 7.5 - 5 * j
        bpy.ops.mesh.primitive_cube_add(size=1, location=(columna_x, 0, columna_z))
        columna = bpy.context.object
        columna.scale = (1, 15, 3)

# Crear las ventanas en todas las fachadas
ventana_size = 2.5
for i in range(4):
    for j in range(6):
        ventana_x = -20 + 8 * i + 4
        ventana_z = 7.5 - 5 * j - 1.25
        bpy.ops.mesh.primitive_cube_add(size=ventana_size, location=(ventana_x, 0, ventana_z))
        ventana = bpy.context.object
        ventana.scale = (ventana_size, ventana_size, ventana_size)

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)