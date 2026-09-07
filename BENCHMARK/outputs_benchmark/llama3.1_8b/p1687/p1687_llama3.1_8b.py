import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del tramo de acera y la calzada
longitud_acera = 10
ancho_acera = 2
alto_calzada = 0.1
ancho_calzada = 3

# Crea el tramo de acera
bpy.ops.mesh.primitive_rectangular_mesh_add(size=ancho_acera, depth=longitud_acera, enter_editmode=False)
objeto_acera = bpy.context.active_object
objeto_acera.location = mathutils.Vector((0, 0, 0))
objeto_acera.scale = (1, ancho_acera, 1)

# Crea la calzada de asfalto
bpy.ops.mesh.primitive_rectangular_mesh_add(size=ancho_calzada, depth=longitud_acera, enter_editmode=False)
objeto_calzada = bpy.context.active_object
objeto_calzada.location = mathutils.Vector((0, ancho_acera + 0.5 * ancho_calzada, alto_calzada))
objeto_calzada.scale = (1, ancho_calzada, 1)

# Crea la baranda metálica
bpy.ops.mesh.primitive_cube_add(size=0.2, enter_editmode=False)
objeto_baranda = bpy.context.active_object
objeto_baranda.location = mathutils.Vector((0, ancho_acera + 0.5 * ancho_calzada - 0.1, alto_calzada))
objeto_baranda.scale = (longitud_acera, 0.2, 0.2)

# Ajusta la altura de la baranda
bpy.ops.transform.resize(value=(longitud_acera, 0.2, 0.2), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

# Ajusta la posición de la baranda
bpy.ops.transform.translate(value=(0, ancho_acera + 0.5 * ancho_calzada - 0.1, alto_calzada), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1)

# Guarda el archivo .blend si se especificó la ruta
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])