import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Parámetros de la escalera
huella = 0.28
contrahuella = 0.18
ancho = 1.0
num_peldaños = 12

# Crear el tramo recto de la escalera
bpy.ops.mesh.primitive_cube_add(size=huella, location=(0, 0, -contrahuella * num_peldaños / 2))
escalera = bpy.context.object

# Añadir modificador de array para los peldaños
bpy.ops.object.modifier_add(type='ARRAY')
array_mod = escalera.modifiers['Array']
array_mod.count = num_peldaños + 1
array_mod.relative_offset_displace[0] = huella

# Añadir modificador de mirror para el ancho del tramo
bpy.ops.object.modifier_add(type='MIRROR')
mirror_mod = escalera.modifiers['Mirror']
mirror_mod.axis = 'X'

# Aplicar los modificadores
bpy.context.view_layer.objects.active = escalera
bpy.ops.object.convert(target='MESH')
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Guardar el archivo si la variable de entorno BLEND_OUT está definida
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])