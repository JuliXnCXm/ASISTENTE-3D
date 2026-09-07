import bpy
import bmesh

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las propiedades del edificio
ancho = 20
fondo = 15
altura_piso = 3
num_pisos = 5

# Crea el cuerpo principal del edificio
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(0, 0, altura_piso))
cuerpo_principal = bpy.context.active_object
cuerpo_principal.name = "Cuerpo Principal"

# Crea las columnas estructurales
for i in range(num_pisos):
    columna = bpy.ops.mesh.primitive_cube_add(size=ancho/2, location=(0, 0, altura_piso*i + ancho/4))
    columna.name = f"Columna {i+1}"

# Crea la retícula de ventanas
for i in range(num_pisos):
    for j in range(int(ancho/3)):
        ventana = bpy.ops.mesh.primitive_cube_add(size=ancho/6, location=(j*ancho/3 - ancho/12, 0, altura_piso*i + ancho/4))
        ventana.name = f"Vidriera {i+1}_{j+1}"

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])