import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear la copa del árbol
bpy.ops.mesh.primitive_circle_add(radius=2, location=(0, 0, 4))
copa = bpy.context.object

# Crear el tronco del árbol
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=2.5, location=(0, 0, 1))
tronco = bpy.context.object

# Unir la copa y el tronco
obj = bpy.data.objects.new("Arbol", None)
bpy.context.collection.objects.link(copa)
bpy.context.collection.objects.link(tronco)
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.object.join()

# Eliminar los objetos originales
bpy.data.objects.remove(copa, do_unlink=True)
bpy.data.objects.remove(tronco, do_unlink=True)

# Guardar el archivo si la variable de entorno BLEND_OUT existe
import os
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])