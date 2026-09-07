import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las propiedades del edificio
ancho = 15  # metros
alto = 10   # metros
num_pisos = 3
espacio_entre_columnas = 2.5  # metros

# Crea el suelo
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(0, 0, -1))
bpy.context.active_object.name = "Suelo"
bpy.context.object.scale[2] = alto

# Crea las columnas
for i in range(-int(ancho/espacio_entre_columnas), int(ancho/espacio_entre_columnas)+1):
    bpy.ops.mesh.primitive_cube_add(size=alto, location=(i*espacio_entre_columnas, 0, -1))
    bpy.context.active_object.name = f"Columna_{i}"
    bpy.context.object.scale[0] = ancho
    bpy.context.object.scale[2] = alto

# Crea las ventanas
for i in range(-int(ancho/espacio_entre_columnas), int(ancho/espacio_entre_columnas)+1):
    for j in range(1, num_pisos+1):
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=(i*espacio_entre_columnas, 0, -j-1))
        bpy.context.active_object.name = f"Ventana_{i}_{j}"
        bpy.context.object.scale[2] = alto/num_pisos
        bpy.context.object.location[2] += (alto/num_pisos) * j

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])