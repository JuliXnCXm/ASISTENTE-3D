import bpy
import os

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Dimensiones del muro
longitud = 5.0  # metros
altura = 2.8  # metros
espesor = 0.15  # metros

# Crear la geometría del muro
bpy.ops.mesh.primitive_plane_add(size=longitud, enter_editmode=False, align='WORLD', location=(0, 0, altura/2), scale=(1, 1, 1))
muro_plane = bpy.context.object
muro_plane.name = "Muro"

# Escalar el plano para obtener el espesor
muro_plane.scale[0] = 1.0
muro_plane.scale[1] = espesor
muro_plane.scale[2] = 1.0

# Aplicar la escala
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Subdividir el muro para poder extrudir
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=1)
bpy.ops.object.mode_set(mode='OBJECT')

# Extruir el muro para darle altura
bpy.ops.object.transform_apply(location=False, rotation=False, scale=False)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, altura)})
bpy.ops.object.mode_set(mode='OBJECT')


# Centrar el muro en el origen
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

# Guardar el archivo .blend si la variable de entorno BLEND_OUT está definida
if "BLEND_OUT" in os.environ:
    blend_out_path = os.environ["BLEND_OUT"]
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)