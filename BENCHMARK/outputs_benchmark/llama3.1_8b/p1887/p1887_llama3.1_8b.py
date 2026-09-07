import bpy
import mathutils

# Limpiar la escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Definir las dimensiones de la oficina en metros
oficina_dimensiones = 3, 4, 2.5

# Crear el suelo de la oficina
bpy.ops.mesh.primitive_plane_add(size=oficina_dimensiones[0], location=(0, 0, -1))

# Crear el techo de la oficina
bpy.ops.mesh.primitive_plane_add(size=oficina_dimensiones[0], location=(0, 0, oficina_dimensiones[2]))

# Crear las paredes de la oficina
for i in range(4):
    bpy.ops.mesh.primitive_plane_add(size=oficina_dimensiones[1], location=(-oficina_dimensiones[0]/2 if i % 2 == 0 else oficina_dimensiones[0]/2, -oficina_dimensiones[1]/2 if i < 2 else oficina_dimensiones[1]/2, 0))

# Crear el escritorio en forma de L
escritorio_dimensiones = 1.5, 0.8, 0.6

bpy.ops.mesh.primitive_cube_add(size=escritorio_dimensiones[0], location=(-oficina_dimensiones[0]/2 + escritorio_dimensiones[0]/2, oficina_dimensiones[1]/2 - escritorio_dimensiones[1]/2, 0))
bpy.context.active_object.scale((1.5, 0.8, 0.6))

# Crear la silla de oficina
silla_dimensiones = 0.4, 0.3, 0.7

bpy.ops.mesh.primitive_cube_add(size=silla_dimensiones[0], location=(-oficina_dimensiones[0]/2 + escritorio_dimensiones[0] + silla_dimensiones[0]/2, oficina_dimensiones[1]/2 - escritorio_dimensiones[1] - silla_dimensiones[1]/2, 0))
bpy.context.active_object.scale((0.4, 0.3, 0.7))

# Crear la estantería de pared
estanteria_dimensiones = 1, 0.5, 1

bpy.ops.mesh.primitive_plane_add(size=estanteria_dimensiones[0], location=(-oficina_dimensiones[0]/2 + escritorio_dimensiones[0] + estanteria_dimensiones[0]/2, oficina_dimensiones[1]/2 - escritorio_dimensiones[1] - estanteria_dimensiones[1]/2, 0))
bpy.context.active_object.scale((1, 0.5, 1))

# Agregar un modificador para dar forma a la estantería
bpy.ops.object.modifier_add(type='ARRAY')
bpy.context.active_object.modifiers[-1].name = 'Estanteria'
bpy.context.active_object.modifiers['Estanteria'].use_merge = True

# Aplicar el modificador
bpy.ops.object.modifier_apply(modifier='Estanteria')

# Guardar la escena si se especifica un archivo de salida
if 'BLEND_OUT' in bpy.context.scene:
    bpy.ops.wm.save_mainfile(filepath=bpy.context.scene['BLEND_OUT'])