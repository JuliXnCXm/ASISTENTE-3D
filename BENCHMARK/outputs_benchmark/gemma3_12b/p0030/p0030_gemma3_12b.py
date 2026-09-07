import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones del muro en metros
largo = 5.0
alto = 2.7
espesor = 0.15

# Crear la geometría del muro
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
muro = bpy.context.object
muro.name = "Muro"
muro.scale = (largo/2, espesor/2, alto/2)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Subdividir el muro para permitir la extrusión
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=1)
bpy.ops.object.mode_set(mode='OBJECT')

# Extruir el muro
bpy.ops.object.transform_apply(location=False, rotation=False, scale=False)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 0)})
bpy.ops.object.mode_set(mode='OBJECT')

# Guardar el archivo .blend si BLEND_OUT está definido
if "BLEND_OUT" in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["BLEND_OUT"])