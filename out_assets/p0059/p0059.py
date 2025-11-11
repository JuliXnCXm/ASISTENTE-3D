import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho_total = 1.5
alto_total = 1.2
grosor_marco = 0.08
profundidad_marco = 0.1
espesor_vidrio = 0.01

# Crear un Empty para agrupar las partes
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
ventana_parent = bpy.context.active_object
ventana_parent.name = 'VentanaFija'

# Crear pieza superior del marco
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, alto_total/2 - grosor_marco/2), scale=(ancho_total, profundidad_marco, grosor_marco))
bpy.context.active_object.parent = ventana_parent

# Crear pieza inferior del marco
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -alto_total/2 + grosor_marco/2), scale=(ancho_total, profundidad_marco, grosor_marco))
bpy.context.active_object.parent = ventana_parent

# Crear pieza izquierda del marco
bpy.ops.mesh.primitive_cube_add(size=1, location=(-ancho_total/2 + grosor_marco/2, 0, 0), scale=(grosor_marco, profundidad_marco, alto_total - 2*grosor_marco))
bpy.context.active_object.parent = ventana_parent

# Crear pieza derecha del marco
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho_total/2 - grosor_marco/2, 0, 0), scale=(grosor_marco, profundidad_marco, alto_total - 2*grosor_marco))
bpy.context.active_object.parent = ventana_parent

# Crear panel de vidrio
ancho_vidrio = ancho_total - 2 * grosor_marco
alto_vidrio = alto_total - 2 * grosor_marco
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0), scale=(ancho_vidrio, espesor_vidrio, alto_vidrio))
bpy.context.active_object.name = 'PanelVidrio'
bpy.context.active_object.parent = ventana_parent