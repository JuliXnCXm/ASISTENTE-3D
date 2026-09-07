import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones del edificio
pisos = 5
ancho = 20
fondo = 15

# Crear los pisos
for piso in range(pisos):
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, location=(0, 0, piso * 3))
    floor = bpy.context.object
    floor.scale = (ancho, fondo, 0.5)
    floor.name = f"Floor_{piso+1}"

# Crear las columnas estructurales
columna_ancho = 2
columna_fondo = 2
columna_espacio = 3

for i in range(1, int(ancho / columna_espacio) + 1):
    for j in range(1, int(fondo / columna_espacio) + 1):
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, location=(i * columna_espacio - ancho/2, j * columna_espacio - fondo/2, 0))
        column = bpy.context.object
        column.scale = (columna_ancho, columna_fondo, pisos * 3)
        column.name = f"Column_{i}_{j}"

# Crear la retícula de ventanas
ventana_ancho = 1.5
ventana_fondo = 1.5

for i in range(2, int(ancho / ventana_espacio) + 1):
    for j in range(2, int(fondo / ventana_espacio) + 1):
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, location=(i * ventana_espacio - ancho/2, j * ventana_espacio - fondo/2, 3))
        window = bpy.context.object
        window.scale = (ventana_ancho, ventana_fondo, 1.5)
        window.name = f"Window_{i}_{j}"

# Guardar el archivo .blend si la variable BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)