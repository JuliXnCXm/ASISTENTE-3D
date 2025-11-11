import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho = 1.2
alto = 1.5
grosor_marco = 0.05
profundidad_marco = 0.1
grosor_vidrio = 0.01

# Crear pieza superior del marco
bpy.ops.mesh.primitive_cube_add(location=(0, 0, alto - grosor_marco / 2), scale=(ancho / 2, profundidad_marco / 2, grosor_marco / 2))
bpy.context.object.name = "MarcoSuperior"

# Crear pieza inferior del marco
bpy.ops.mesh.primitive_cube_add(location=(0, 0, grosor_marco / 2), scale=(ancho / 2, profundidad_marco / 2, grosor_marco / 2))
bpy.context.object.name = "MarcoInferior"

# Crear pieza izquierda del marco
bpy.ops.mesh.primitive_cube_add(location=(-ancho / 2 + grosor_marco / 2, 0, alto / 2), scale=(grosor_marco / 2, profundidad_marco / 2, (alto - 2 * grosor_marco) / 2))
bpy.context.object.name = "MarcoIzquierdo"

# Crear pieza derecha del marco
bpy.ops.mesh.primitive_cube_add(location=(ancho / 2 - grosor_marco / 2, 0, alto / 2), scale=(grosor_marco / 2, profundidad_marco / 2, (alto - 2 * grosor_marco) / 2))
bpy.context.object.name = "MarcoDerecho"

# Crear panel de vidrio
ancho_vidrio = ancho - 2 * grosor_marco
alto_vidrio = alto - 2 * grosor_marco
bpy.ops.mesh.primitive_cube_add(location=(0, 0, alto / 2), scale=(ancho_vidrio / 2, grosor_vidrio / 2, alto_vidrio / 2))
bpy.context.object.name = "PanelVidrio"