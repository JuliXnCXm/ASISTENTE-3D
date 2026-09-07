import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la escalera
num_peldaños = 15
ancho_peldaño = 1.0
huella = 0.3
contrahuella = 0.18

# Altura total de la escalera
altura_total = num_peldaños * contrahuella

# Longitud total de la escalera
longitud_total = num_peldaños * huella

# Crear la escalera
for i in range(num_peldaños):
    # Calcular la posición del peldaño
    x = i * huella
    y = 0.0
    z = i * contrahuella

    # Crear la geometría del peldaño
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(x, y, z), scale=(ancho_peldaño, huella, contrahuella))
    peldaño = bpy.context.object
    peldaño.name = f"Peldaño_{i+1}"

# Ajustar el origen del objeto a la geometría
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

# Escalar la escalera para que esté en metros
bpy.ops.transform.resize(value=(1, 1, 0.001))

# Guardar el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])