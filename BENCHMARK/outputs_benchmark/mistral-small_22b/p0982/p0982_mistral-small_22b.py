import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el sofá de cuero de 3 plazas
def create_sofa():
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    sofa = bpy.context.object
    sofa.name = "Sofa"

    # Crear los cojines del sofá
    for i in range(3):
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=(i * 1.2 - 1.8, 0, 0))
        cojin = bpy.context.object
        cojin.name = f"Cojin_{i}"
        sofa.objects.link(cojin)

    # Crear el respaldo del sofá
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -2))
    respaldo = bpy.context.object
    respaldo.name = "Respaldo"
    sofa.objects.link(respaldo)

create_sofa()

# Crear la mesa de centro de madera de nogal
def create_mesa():
    bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 0, -1))
    mesa = bpy.context.object
    mesa.name = "Mesa"

create_mesa()

# Guardar el archivo .blend si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as(filepath=os.environ['BLEND_OUT'])