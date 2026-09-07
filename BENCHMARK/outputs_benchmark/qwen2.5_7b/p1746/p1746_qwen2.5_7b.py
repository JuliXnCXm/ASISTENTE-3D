import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones del edificio
plantas = 5
ancho_planta = 20
largo_planta = 30
altura_planta = 4.5
espacio_entre_columnas = 4
altura_columna = 10

# Crear la base de asfalto
bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, -2))
base = bpy.context.object
base.scale = (largo_planta * 3, ancho_planta * 3, 0.1)

# Crear las columnas
for i in range(int(largo_planta / espacio_entre_columnas) + 1):
    for j in range(int(ancho_planta / espacio_entre_columnas) + 1):
        x = -largo_planta / 2 + i * espacio_entre_columnas
        z = -ancho_planta / 2 + j * espacio_entre_columnas
        bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=altura_columna, location=(x, 0, z))
        columna = bpy.context.object
        columna.scale = (1, 1, 1)

# Crear las plantas superiores
for i in range(plantas):
    planta = bpy.ops.mesh.primitive_cube_add(size=45, location=(0, 0, i * altura_planta + altura_planta / 2))
    planta_obj = bpy.context.object
    planta_obj.scale = (largo_planta, ancho_planta, altura_planta)

# Crear la fachada de estuco
fachada = bpy.ops.mesh.primitive_cube_add(size=45, location=(0, 0, plantas * altura_planta + altura_planta / 2))
fachada_obj = bpy.context.object
fachada_obj.scale = (largo_planta, ancho_planta, 1)

# Crear las ventanas en la fachada principal
for i in range(int(largo_planta / espacio_entre_columnas) - 1):
    for j in range(int(ancho_planta / espacio_entre_columnas) - 1):
        x = -largo_planta / 2 + (i + 0.5) * espacio_entre_columnas
        z = -ancho_planta / 2 + (j + 0.5) * espacio_entre_columnas
        ventana = bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, plantas * altura_planta + altura_planta / 2))
        ventana_obj = bpy.context.object
        ventana_obj.scale = (espacio_entre_columnas / 4, espacio_entre_columnas / 4, 1)

# Guardar el archivo si existe BLEND_OUT
if "BLEND_OUT" in os.environ:
    blend_out = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out)