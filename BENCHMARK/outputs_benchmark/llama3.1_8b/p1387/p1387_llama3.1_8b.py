import bpy
import mathutils

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Define las dimensiones de la fachada
ancho = 10
alto = 6
puerta_ancho = 2
ventana_ancho = 1.5
ventana_altura = 3

# Crea el bloque base de la fachada
bpy.ops.mesh.primitive_cube_add(size=ancho, location=(0, 0, alto/2))
objeto_base = bpy.context.active_object
objeto_base.name = "Fachada"

# Crea la puerta
bpy.ops.mesh.primitive_cube_add(size=puerta_ancho, location=(-ancho/2 + puerta_ancho/2, 0, alto/2 - 1))
objeto_puerta = bpy.context.active_object
objeto_puerta.name = "Puerta"

# Crea las ventanas
bpy.ops.mesh.primitive_cube_add(size=ventana_ancho, location=(-ancho/4 + ventana_ancho/2, 0, alto/2 - 1.5))
objeto_ventana1 = bpy.context.active_object
objeto_ventana1.name = "Ventana Izquierda"

bpy.ops.mesh.primitive_cube_add(size=ventana_ancho, location=(ancho/4 - ventana_ancho/2, 0, alto/2 - 1.5))
objeto_ventana2 = bpy.context.active_object
objeto_ventana2.name = "Ventana Derecha"

# Alinea las ventanas y la puerta con el bloque base
bpy.ops.object.select_all(action='DESELECT')
objeto_base.select_set(True)
bpy.context.view_layer.objects.active = objeto_base

bpy.ops.object.modifier_add(type='ARRAY')
modificador_array = objeto_base.modifiers[-1]
modificador_array.use_merge = True
modificador_array.merge_mode = 'COLLAPSE'

bpy.ops.object.modifier_apply(modifier=modificador_array.name)

# Alinea la puerta y las ventanas con el bloque base
objeto_puerta.select_set(True)
bpy.context.view_layer.objects.active = objeto_base

modificador_array = objeto_base.modifiers[-1]
modificador_array.use_merge = True
modificador_array.merge_mode = 'COLLAPSE'

bpy.ops.object.modifier_apply(modifier=modificador_array.name)

objeto_ventana1.select_set(True)
bpy.context.view_layer.objects.active = objeto_base

modificador_array = objeto_base.modifiers[-1]
modificador_array.use_merge = True
modificador_array.merge_mode = 'COLLAPSE'

bpy.ops.object.modifier_apply(modifier=modificador_array.name)

objeto_ventana2.select_set(True)
bpy.context.view_layer.objects.active = objeto_base

modificador_array = objeto_base.modifiers[-1]
modificador_array.use_merge = True
modificador_array.merge_mode = 'COLLAPSE'

bpy.ops.object.modifier_apply(modifier=modificador_array.name)

# Guarda el archivo .blend si se especificó la variable de entorno BLEND_OUT
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene.BLEND_OUT)