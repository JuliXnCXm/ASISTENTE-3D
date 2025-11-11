import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones de la habitación y muros
ancho_x = 5.0
fondo_y = 4.0
alto_z = 2.5
espesor = 0.2

# Muro Norte (paralelo a X)
bpy.ops.mesh.primitive_cube_add(
    location=(0, (fondo_y - espesor) / 2.0, alto_z / 2.0),
    scale=(ancho_x, espesor, alto_z))
bpy.context.object.name = 'MuroNorte'

# Muro Sur (paralelo a X)
bpy.ops.mesh.primitive_cube_add(
    location=(0, -(fondo_y - espesor) / 2.0, alto_z / 2.0),
    scale=(ancho_x, espesor, alto_z))
bpy.context.object.name = 'MuroSur'

# Muro Este (paralelo a Y)
bpy.ops.mesh.primitive_cube_add(
    location=((ancho_x - espesor) / 2.0, 0, alto_z / 2.0),
    scale=(espesor, fondo_y - 2 * espesor, alto_z))
bpy.context.object.name = 'MuroEste'

# Muro Oeste (paralelo a Y)
bpy.ops.mesh.primitive_cube_add(
    location=(-(ancho_x - espesor) / 2.0, 0, alto_z / 2.0),
    scale=(espesor, fondo_y - 2 * espesor, alto_z))
bpy.context.object.name = 'MuroOeste'