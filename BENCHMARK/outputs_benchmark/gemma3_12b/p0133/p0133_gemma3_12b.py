import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la escalera
num_peldaños = 15
ancho_peldaño = 1.0
profundidad_peldaño = 0.3
altura_contrahuella = 0.18

# Calcular la altura total de la escalera
altura_total = num_peldaños * altura_contrahuella

# Crear la escalera
for i in range(num_peldaños):
    # Calcular la posición del peldaño
    x = i * profundidad_peldaño
    y = 0.0
    z = i * altura_contrahuella

    # Crear la geometría del peldaño
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(x, y, z), scale=(ancho_peldaño, profundidad_peldaño, 0.05))
    peldaño = bpy.context.object
    peldaño.name = f"Peldaño_{i+1}"

# Opcional: Guardar el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])