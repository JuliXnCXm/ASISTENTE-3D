import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo = 2.0
ancho = 0.8
alto = 0.6
grosor = 0.05

# Crear el suelo
bpy.ops.mesh.primitive_cube_add(location=(0, 0, grosor / 2), scale=(largo, ancho, grosor))
bpy.context.object.name = "Jardinera_Suelo"

# Pared frontal
bpy.ops.mesh.primitive_cube_add(location=(0, (ancho - grosor) / 2, (alto + grosor) / 2), scale=(largo, grosor, alto - grosor))
bpy.context.object.name = "Jardinera_ParedFrontal"

# Pared trasera
bpy.ops.mesh.primitive_cube_add(location=(0, -(ancho - grosor) / 2, (alto + grosor) / 2), scale=(largo, grosor, alto - grosor))
bpy.context.object.name = "Jardinera_ParedTrasera"

# Pared izquierda
bpy.ops.mesh.primitive_cube_add(location=(-(largo - grosor) / 2, 0, (alto + grosor) / 2), scale=(grosor, ancho - 2 * grosor, alto - grosor))
bpy.context.object.name = "Jardinera_ParedIzquierda"

# Pared derecha
bpy.ops.mesh.primitive_cube_add(location=((largo - grosor) / 2, 0, (alto + grosor) / 2), scale=(grosor, ancho - 2 * grosor, alto - grosor))
bpy.context.object.name = "Jardinera_ParedDerecha"