import bpy

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear el tronco del árbol
tronco = bpy.data.objects.new("Tronco", None)
bpy.context.collection.objects.link(tronco)

bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=2.5, location=(0, 0, 1.25))
bpy.context.object.name = "TroncoObj"
tronco.data = bpy.data.objects["TroncoObj"].data

# Crear la copa del árbol
copa = bpy.data.objects.new("Copa", None)
bpy.context.collection.objects.link(copa)

bpy.ops.mesh.primitive_uv_sphere_add(radius=2, location=(0, 0, 4))
bpy.context.object.name = "CopaObj"
copa.data = bpy.data.objects["CopaObj"].data

# Alinear la copa encima del tronco
copa.location = (0, 0, 1.75)

# Guardar el archivo .blend si existe BLEND_OUT en las variables de entorno
if "BLEND_OUT" in bpy.context.scene:
    blend_out_path = bpy.context.scene.BLEND_OUT
    bpy.ops.wm.save_as_mainfile(filepath=blend_out_path)