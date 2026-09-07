import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la terraza
ancho = 6
largo = 4
alto = 0.5  # altura de la baranda

# Crea el plano de la terraza
bpy.ops.mesh.primitive_plane_add(size=ancho, location=(0, -largo/2, alto))

# Duplica y gira para crear la otra mitad de la terraza
obj = bpy.context.active_object
obj.select_set(True)
bpy.ops.object.duplicate_move_linked()
obj.location = (ancho, 0, 0)
obj.rotation_euler = mathutils.Euler((math.pi/2, 0, 0), 'XYZ')

# Crea la baranda
bpy.ops.mesh.primitive_cube_add(size=alto, location=(0, -largo/2 + ancho/4, alto))
obj.select_set(True)
bpy.ops.object.duplicate_move_linked()
obj.location = (ancho/2, 0, 0)

# Ajusta la altura de la baranda
obj.scale = (1, 1, alto / 0.5)

# Guarda el archivo .blend si se especificó una ruta de salida
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])