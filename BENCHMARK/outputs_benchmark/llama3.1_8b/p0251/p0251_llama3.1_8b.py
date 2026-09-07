import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones del bolardo
alto = 0.9  # metros
diametro = 0.2  # metros

# Crea un nuevo objeto cilíndrico en el origen de coordenadas
bolardo = bpy.data.objects.new("Bolardo", None)
bolardo.location = mathutils.Vector((0, 0, 0))
bolardo.scale = (1, diametro, alto)

# Agrega la geometría del bolardo
bpy.context.collection.objects.link(bolardo)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.modifier_add(type='ARRAY')
bpy.context.active_object.modifiers['Array'].use_merge = True
bpy.context.active_object.modifiers['Array'].merge_distance = 0.001

# Aplica la geometría del bolardo
bpy.ops.object.modifier_apply(modifier="Array")

# Si existe la variable de entorno BLEND_OUT, guarda el archivo .blend
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_mainfile(filepath=os.environ['BLEND_OUT'])