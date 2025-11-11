import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones interiores y de elementos
dim_x_int = 6.0
dim_y_int = 4.0
altura = 3.0
espesor_muro = 0.20
espesor_losa = 0.20

# Dimensiones exteriores
dim_x_ext = dim_x_int + 2 * espesor_muro
dim_y_ext = dim_y_int + espesor_muro # Un muro es compartido

# Crear losa de piso
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(dim_x_ext / 2 - espesor_muro/2, dim_y_ext / 2, -espesor_losa / 2),
    scale=(dim_x_ext, dim_y_ext + espesor_muro, espesor_losa)
)
bpy.context.active_object.name = 'LosaHabitacion'

# Crear muro Norte (al fondo)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(dim_x_ext / 2 - espesor_muro/2, dim_y_int + espesor_muro / 2, altura / 2),
    scale=(dim_x_ext, espesor_muro, altura)
)
bpy.context.active_object.name = 'MuroNorte'

# Crear muro Sur (frontal)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(dim_x_ext / 2 - espesor_muro/2, -espesor_muro / 2, altura / 2),
    scale=(dim_x_ext, espesor_muro, altura)
)
bpy.context.active_object.name = 'MuroSur'

# Crear muro Este (derecha)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(dim_x_int + espesor_muro / 2, dim_y_int / 2, altura / 2),
    scale=(espesor_muro, dim_y_int, altura)
)
bpy.context.active_object.name = 'MuroEste'

# Crear muro Oeste (izquierda)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-espesor_muro / 2, dim_y_int / 2, altura / 2),
    scale=(espesor_muro, dim_y_int, altura)
)
bpy.context.active_object.name = 'MuroOeste'