import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la escalera
num_peldaños = 12
huella = 0.28  # Profundidad de la huella en metros
contrahuella = 0.18  # Altura de la contrahuella en metros
ancho_tramo = 1.0  # Ancho del tramo en metros

# Altura total de la escalera
altura_total = num_peldaños * contrahuella

# Crear la escalera
for i in range(num_peldaños):
    # Calcular la posición de la huella
    x = i * huella
    y = 0.0
    z = i * contrahuella

    # Crear la huella
    bpy.ops.mesh.primitive_cube_add(size=huella, location=(x, y, z))
    huella_obj = bpy.context.object
    huella_obj.scale[0] = 1.0
    huella_obj.scale[1] = 1.0
    huella_obj.scale[2] = 0.01  # Grosor de la huella
    huella_obj.name = f"Huella_{i}"

    # Crear la contrahuella
    bpy.ops.mesh.primitive_cube_add(size=ancho_tramo, location=(x + huella/2, y + ancho_tramo/2, z + contrahuella/2))
    contrahuella_obj = bpy.context.object
    contrahuella_obj.scale[0] = 1.0
    contrahuella_obj.scale[1] = 0.01
    contrahuella_obj.scale[2] = 0.01
    contrahuella_obj.name = f"Contrahuela_{i}"

# Opcional: Guardar el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])