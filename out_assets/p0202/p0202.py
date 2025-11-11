import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar escena
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo = 2.5
ancho = 0.6
alto = 0.5
grosor = 0.1

# Crear base
bpy.ops.mesh.primitive_cube_add(location=(0, 0, grosor / 2))
bpy.context.object.scale = (largo / 2, ancho / 2, grosor / 2)
bpy.ops.object.transform_apply(scale=True)

# Crear pared trasera
bpy.ops.mesh.primitive_cube_add(location=(0, -ancho/2 + grosor/2, alto/2))
bpy.context.object.scale = (largo / 2, grosor / 2, alto / 2)
bpy.ops.object.transform_apply(scale=True)

# Crear pared frontal
bpy.ops.mesh.primitive_cube_add(location=(0, ancho/2 - grosor/2, alto/2))
bpy.context.object.scale = (largo / 2, grosor / 2, alto / 2)
bpy.ops.object.transform_apply(scale=True)

# Crear pared izquierda
bpy.ops.mesh.primitive_cube_add(location=(-largo/2 + grosor/2, 0, alto/2))
bpy.context.object.scale = (grosor / 2, (ancho - 2 * grosor) / 2, alto / 2)
bpy.ops.object.transform_apply(scale=True)

# Crear pared derecha
bpy.ops.mesh.primitive_cube_add(location=(largo/2 - grosor/2, 0, alto/2))
bpy.context.object.scale = (grosor / 2, (ancho - 2 * grosor) / 2, alto / 2)
bpy.ops.object.transform_apply(scale=True)