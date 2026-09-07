import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crea un nuevo objeto cilíndrico
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.8, location=(0, 0, 0))

# Obtiene el objeto creado
obj = bpy.context.active_object

# Establece la escala en metros
obj.scale = (0.2 / obj.dimensions.x, 0.2 / obj.dimensions.y, 0.8 / obj.dimensions.z)

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in bpy.context.scene.properties:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene.properties['BLEND_OUT'])