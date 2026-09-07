import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el primer muro de 4m en el eje X
bpy.ops.mesh.primitive_cube_add(size=2.5, location=(2, 0, 1.25))
bpy.context.object.scale = (4, 2.5, 2.5)

# Crear el segundo muro de 3m en el eje Y
bpy.ops.mesh.primitive_cube_add(size=2.5, location=(0, 1.5, 1.25))
bpy.context.object.scale = (2.5, 3, 2.5)

# Guardar la escena si se especifica una ruta de salida
if 'BLEND_OUT' in bpy.context.scene:
    blend_out_path = bpy.context.scene['BLEND_OUT']
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)