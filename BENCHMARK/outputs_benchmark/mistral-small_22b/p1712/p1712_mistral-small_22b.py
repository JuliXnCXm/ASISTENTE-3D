import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Parámetros del edificio
altura = 3 * 4  # 3 pisos de 4 metros cada uno
ancho = 15
profundidad = 10
espacio_ventanas = 2

# Crear el suelo
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, ancho / 2, -profundidad / 2))
bpy.context.object.scale.x = ancho

# Función para crear una ventana
def crear_ventana():
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=(0, 0, 0))
    obj = bpy.context.object
    obj.scale.x = espacio_ventanas
    obj.scale.y = altura - (espacio_ventanas * 2)
    return obj

# Crear las fachadas con ventanas
for i in range(0, ancho, espacio_ventanas):
    for j in range(0, altura, espacio_ventanas):
        bpy.ops.object.select_all(action='DESELECT')
        crear_ventana().location = (i - ancho / 2, j - altura / 2, profundidad / 2)

for i in range(0, ancho, espacio_ventanas):
    for j in range(0, altura, espacio_ventanas):
        bpy.ops.object.select_all(action='DESELECT')
        crear_ventana().location = (i - ancho / 2, j - altura / 2, -profundidad / 2)

# Crear los muros laterales
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho / 2, 0, -profundidad / 2))
bpy.context.object.scale.y = altura

bpy.ops.mesh.primitive_cube_add(size=1, location=(-ancho / 2, 0, -profundidad / 2))
bpy.context.object.scale.y = altura

# Guardar el archivo si BLEND_OUT está definido
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])