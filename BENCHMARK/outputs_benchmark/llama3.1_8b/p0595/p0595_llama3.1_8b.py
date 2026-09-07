import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del edificio
ancho = 15
alto = 10
profundo = 20

# Crea el cuerpo principal del edificio
bpy.ops.mesh.primitive_cube_add(size=alto, location=(0, 0, 0))
objeto_edificio = bpy.context.active_object
objeto_edificio.scale = (ancho, alto, profundo)

# Define las dimensiones de la ventana
ventana_ancho = 1.5
ventana_alto = 2

# Crea una lista para almacenar los objetos de ventanas
objetos_ventanas = []

# Crea las ventanas en la fachada del edificio
for i in range(10):
    for j in range(3):
        # Calcula la posición de la ventana
        x = -ancho / 2 + (i * ventana_ancho)
        y = alto / 2 - (j * ventana_alto)

        # Crea una ventana
        bpy.ops.mesh.primitive_cube_add(size=ventana_alto, location=(x, y, 0))
        objeto_ventana = bpy.context.active_object

        # Ajusta la escala de la ventana para que sea más pequeña
        objeto_ventana.scale = (ventana_ancho / ancho, ventana_alto / alto, 1)

        # Agrega la ventana a la lista
        objetos_ventanas.append(objeto_ventana)

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])