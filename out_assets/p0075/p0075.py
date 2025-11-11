import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho_hueco = 0.9
alto_hueco = 2.1
grosor_marco = 0.05
profundidad_marco = 0.15

# Crear dintel (parte superior)
pos_y_dintel = alto_hueco + grosor_marco / 2.0
ancho_total = ancho_hueco + 2 * grosor_marco
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, pos_y_dintel),
    scale=(ancho_total, profundidad_marco, grosor_marco)
)
bpy.context.object.name = 'Dintel'

# Crear jamba izquierda
pos_x_jamba = -ancho_hueco / 2.0 - grosor_marco / 2.0
bpy.ops.mesh.primitive_cube_add(
    location=(pos_x_jamba, 0, alto_hueco / 2.0),
    scale=(grosor_marco, profundidad_marco, alto_hueco)
)
bpy.context.object.name = 'JambaIzquierda'

# Crear jamba derecha
pos_x_jamba = ancho_hueco / 2.0 + grosor_marco / 2.0
bpy.ops.mesh.primitive_cube_add(
    location=(pos_x_jamba, 0, alto_hueco / 2.0),
    scale=(grosor_marco, profundidad_marco, alto_hueco)
)
bpy.context.object.name = 'JambaDerecha'

# Rotar para que esté vertical en el plano XY
for obj in bpy.context.scene.objects:
    obj.rotation_euler[0] = 1.5708 # 90 grados en radianes
    obj.location.z, obj.location.y = obj.location.y, obj.location.z