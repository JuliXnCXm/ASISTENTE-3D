import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del edificio
ancho = 20
fondo = 15
altura_piso = 3

# Crea el cuerpo principal del edificio
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(0, 0, altura_piso))
cuerpo_principal = bpy.context.active_object
cuerpo_principal.name = "Cuerpo Principal"

# Crea las columnas estructurales
for i in range(5):
    for j in range(int(ancho / 2) + 1):
        columna = bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=fondo, location=(j * 2 - ancho / 2, 0, altura_piso * (i + 1)))
        columna.name = f"Columna {i+1}x{j+1}"

# Crea la retícula de ventanas
for i in range(5):
    for j in range(int(ancho / 2) + 1):
        ventana = bpy.ops.mesh.primitive_cube_add(size=0.5, location=(j * 2 - ancho / 2, 0, altura_piso * (i + 1)))
        ventana.name = f"Ventana {i+1}x{j+1}"

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])