import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones del muro en metros
longitud = 5.0
altura = 2.7
espesor = 0.15

# Crear el muro
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
muro = bpy.context.object
muro.name = "Muro"
muro.scale = (longitud/2, espesor/2, altura/2)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Subdividir el muro para darle altura
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=int(altura / 0.1))
bpy.ops.object.mode_set(mode='OBJECT')

# Ajustar la geometría para que sea un muro sólido
bpy.ops.object.convert(target='MESH')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles(threshold=0.0001)

# Guardar el archivo .blend si BLEND_OUT está definido
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])