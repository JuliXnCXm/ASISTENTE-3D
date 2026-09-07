import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el tronco
bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2.5, location=(0, 0, -1))
tronco = bpy.context.object

# Crear la copa
bpy.ops.mesh.primitive_cone_add(radius1=2, radius2=2, depth=4, location=(0, 0, 1), rotation_euler=(0, 0, 0))
copa = bpy.context.object

# Unir el tronco y la copa en un solo objeto
bpy.ops.object.select_all(action='DESELECT')
tronco.select_set(True)
copa.select_set(True)
bpy.ops.object.join()

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])