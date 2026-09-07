import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones del edificio
pisos = 5
ancho = 20
fondo = 15

# Crear el piso inferior
bpy.ops.mesh.primitive_plane_add(size=ancho, location=(0, 0, -pisos * 3))
piso_inferior = bpy.context.object
piso_inferior.name = "Piso_Inferior"

# Crear los pisos superiores
for i in range(pisos):
    piso_superior = piso_inferior.copy()
    piso_superior.location.z += 3
    bpy.context.collection.objects.link(piso_superior)

# Crear las columnas estructurales
columna_ancho = 1.5
columna_fondo = 1.5

for i in range(0, ancho // columna_ancho + 1):
    for j in range(0, fondo // columna_fondo + 1):
        columna = bpy.ops.mesh.primitive_cube_add(size=2, location=(i * columna_ancho - (ancho / 2), j * columna_fondo - (fondo / 2), -pisos * 3))
        columna_obj = bpy.context.object
        columna_obj.name = f"Columna_{i}_{j}"

# Crear la retícula de ventanas
ventana_ancho = 2
ventana_fondo = 2

for i in range(1, ancho // ventana_ancho):
    for j in range(1, fondo // ventana_fondo):
        ventana = bpy.ops.mesh.primitive_cube_add(size=2, location=(i * ventana_ancho - (ancho / 2) + ventana_ancho / 2, j * ventana_fondo - (fondo / 2) + ventana_fondo / 2, -pisos * 3))
        ventana_obj = bpy.context.object
        ventana_obj.name = f"Ventana_{i}_{j}"

# Guardar el archivo .blend si existe la variable de entorno BLEND_OUT
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)