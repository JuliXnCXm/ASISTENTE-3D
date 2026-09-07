import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la escalera
num_peldaños = 16
ancho_escalera = 1.0  # metros
altura_peldaño = 0.2  # metros (altura total / num_peldaños)
longitud_peldaño = 0.3  # metros
altura_total = altura_peldaño * num_peldaños

# Crear la base
bpy.ops.mesh.primitive_plane_add(size=ancho_escalera, enter_editmode=False, align='WORLD', location=(0, 0, 0))
base = bpy.context.object
base.name = "Base"

# Crear los peldaños
for i in range(num_peldaños):
    bpy.ops.mesh.primitive_cube_add(size=longitud_peldaño, enter_editmode=False, align='WORLD', location=(0, i * longitud_peldaño, altura_peldaño * i))
    peldaño = bpy.context.object
    peldaño.name = f"Peldaño_{i}"
    peldaño.scale[0] = ancho_escalera
    peldaño.scale[2] = 1.0

# Crear la pared de fondo (opcional)
bpy.ops.mesh.primitive_plane_add(size=longitud_peldaño, enter_editmode=False, align='WORLD', location=(0, num_peldaños * longitud_peldaño, altura_total))
pared = bpy.context.object
pared.name = "Pared_Fondo"
pared.scale[0] = ancho_escalera
pared.rotation_euler[0] = 1.5708  # 90 grados en radianes

# Mover la escalera a una posición más alta
escalera_base_z = 2.0
for obj in bpy.data.objects:
    if "Base" in obj.name:
        obj.location[2] = escalera_base_z
    if "Peldaño" in obj.name:
        obj.location[2] += escalera_base_z
    if "Pared_Fondo" in obj.name:
        obj.location[2] += escalera_base_z

# Unir los peldaños (opcional)
# bpy.ops.object.select_all(action='DESELECT')
# for obj in bpy.data.objects:
#     if "Peldaño" in obj.name:
#         obj.select_set(True)
# bpy.ops.object.join()
# bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Guardar el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])