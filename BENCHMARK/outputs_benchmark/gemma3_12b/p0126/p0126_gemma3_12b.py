import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones de la partición
longitud = 4.0
altura = 2.5
espesor = 0.15

# Crear la geometría
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
pared = bpy.context.object
pared.name = "Pared"
pared.scale = (longitud/2, espesor/2, altura/2)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Subdividir para dar grosor
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=1)
bpy.ops.object.mode_set(mode='OBJECT')

# Extruir para dar grosor
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 0)})
bpy.ops.object.mode_set(mode='OBJECT')

# Centrar la pared
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center=True)

# Guardar el archivo .blend si BLEND_OUT está definido
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])