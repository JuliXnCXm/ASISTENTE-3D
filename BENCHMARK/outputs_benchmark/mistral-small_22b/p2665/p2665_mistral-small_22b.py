import bpy

# Limpia la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Variables
huella = 0.28
contrahuella = 0.18
ancho_tramo = 1.0
numero_peldaños = 12
altura_total = huella * numero_peldaños + contrahuella * (numero_peldaños - 1)

# Crear el tramo de escalera
bpy.ops.mesh.primitive_cube_add(size=ancho_tramo, location=(0, 0, altura_total / 2))
escalera = bpy.context.object

# Añadir modificador Array para los peldaños
bpy.ops.object.modifier_add(type='ARRAY')
array_mod = escalera.modifiers['Array']
array_mod.count = numero_peldaños + 1
array_mod.relative_offset_displace[0] = 0
array_mod.relative_offset_displace[2] = huella

# Añadir modificador Mirror para simetría
bpy.ops.object.modifier_add(type='MIRROR')
mirror_mod = escalera.modifiers['Mirror']
mirror_mod.axis = 'X'

# Aplicar los modificadores
bpy.context.view_layer.objects.active = escalera
bpy.ops.object.convert(target='MESH')
bpy.ops.object.select_all(action='DESELECT')
escalera.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')

# Guardar el archivo si existe la variable de entorno BLEND_OUT
if 'BLEND_OUT' in os.environ:
    bpy.ops.wm.save_as_mainfile(filepath=os.environ['BLEND_OUT'])