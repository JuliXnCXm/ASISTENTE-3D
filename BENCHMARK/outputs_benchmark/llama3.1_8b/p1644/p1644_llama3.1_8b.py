import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del edificio
ancho = 15
alto = 20
num_pisos = 5

# Crea el suelo
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
bpy.context.active_object.name = "Suelo"
bpy.context.object.scale = (ancho, alto, 0.01)

# Crea las columnas estructurales
for i in range(-7, 8):
    for j in range(-3, 4):
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=(i * 2, j * 2, -1))
        bpy.context.active_object.name = f"Columna_{i}_{j}"
        bpy.context.object.scale = (0.5, 0.5, 10)

# Crea las paredes exteriores
for i in range(-7, 8):
    for j in range(-3, 4):
        if abs(i) > 6 or abs(j) > 2:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(i * 2, j * 2, -0.5))
            bpy.context.active_object.name = f"Pared_{i}_{j}"
            bpy.context.object.scale = (ancho, alto, 0.01)

# Crea la plaza de acceso
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -2))
bpy.context.active_object.name = "Plaza"
bpy.context.object.scale = (15, 20, 0.01)

# Crea las ventanas y puertas
for i in range(-7, 8):
    for j in range(-3, 4):
        if abs(i) > 6 or abs(j) > 2:
            bpy.ops.mesh.primitive_cube_add(size=0.5, location=(i * 2 + 1, j * 2 + 1, -0.5))
            bpy.context.active_object.name = f"Ventana_{i}_{j}"
            bpy.context.object.scale = (1, 1, 0.01)

# Crea la fachada de cristal
for i in range(-7, 8):
    for j in range(-3, 4):
        if abs(i) > 6 or abs(j) > 2:
            bpy.ops.mesh.primitive_cube_add(size=1, location=(i * 2 + 1, j * 2 + 1, -0.5))
            bpy.context.active_object.name = f"Fachada_{i}_{j}"
            bpy.context.object.scale = (ancho, alto, 0.01)
            bpy.ops.mesh.primitive_uv_sphere_add(size=1, location=(i * 2 + 1, j * 2 + 1, -0.5))
            bpy.context.active_object.name = f"Cristal_{i}_{j}"
            bpy.context.object.scale = (ancho, alto, 0.01)

# Guarda el archivo .blend si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])