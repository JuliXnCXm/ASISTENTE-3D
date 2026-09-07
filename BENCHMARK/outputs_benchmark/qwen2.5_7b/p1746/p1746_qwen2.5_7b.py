import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del edificio
ancho = 20
largo = 30
altura_planta = 4
num_plantas = 5

# Crea el suelo de asfalto
bpy.ops.mesh.primitive_plane_add(size=100, location=(0, 0, -1))
asfalto = bpy.context.object
asfalto.scale = (ancho * 2, largo * 2, 0.1)
asfalto.name = "Asfalto"

# Crea las plantas del edificio
for i in range(num_plantas):
    planta = bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, i * altura_planta))
    planta_obj = bpy.context.object
    planta_obj.scale = (ancho, largo, altura_planta)
    planta_obj.name = f"Planta_{i+1}"

# Crea las columnas visibles
columna_height = altura_planta / 2
columna_width = 0.5

for i in range(4):
    for j in range(3):
        columna = bpy.ops.mesh.primitive_cube_add(size=1, location=(j * (ancho - columna_width) + columna_width / 2, i * (largo - columna_width) + columna_width / 2, altura_planta / 2))
        columna_obj = bpy.context.object
        columna_obj.scale = (columna_width, columna_width, columna_height)
        columna_obj.name = f"Columna_{i*3+j+1}"

# Crea las ventanas en la fachada principal
ventana_size = 4

for i in range(2):
    for j in range(5):
        ventana = bpy.ops.mesh.primitive_cube_add(size=1, location=(j * (ancho - ventana_size) + ventana_size / 2, i * (largo - ventana_size) + largo - ventana_size / 2, altura_planta))
        ventana_obj = bpy.context.object
        ventana_obj.scale = (ventana_size, ventana_size, altura_planta)
        ventana_obj.name = f"Ventana_{i*5+j+1}"

# Crea la fachada de estuco
estuco_thickness = 0.2

for i in range(4):
    for j in range(3):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(j * (ancho - estuco_thickness) + estuco_thickness / 2, i * (largo - estuco_thickness) + largo - estuco_thickness / 2, altura_planta))
        estuco_obj = bpy.context.object
        estuco_obj.scale = (estuco_thickness, estuco_thickness, estuco_thickness)
        estuco_obj.name = f"Estuco_{i*3+j+1}"

# Guarda el archivo si la variable de entorno BLEND_OUT existe
import os
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)