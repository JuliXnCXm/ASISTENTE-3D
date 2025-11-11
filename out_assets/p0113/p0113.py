import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
dim_x_int = 4.0
dim_y_int = 5.0
altura_int = 2.8
espesor_muro = 0.15
espesor_losa = 0.2

# Dimensiones exteriores
dim_x_ext = dim_x_int + 2 * espesor_muro
dim_y_ext = dim_y_int + 2 * espesor_muro

# Crear Losa de suelo
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, -espesor_losa / 2),
    scale=(dim_x_ext, dim_y_ext, espesor_losa)
)

# Crear Muro Norte (+Y)
bpy.ops.mesh.primitive_cube_add(
    location=(0, dim_y_int / 2 + espesor_muro / 2, altura_int / 2),
    scale=(dim_x_ext, espesor_muro, altura_int)
)

# Crear Muro Sur (-Y)
bpy.ops.mesh.primitive_cube_add(
    location=(0, -dim_y_int / 2 - espesor_muro / 2, altura_int / 2),
    scale=(dim_x_ext, espesor_muro, altura_int)
)

# Crear Muro Este (+X)
bpy.ops.mesh.primitive_cube_add(
    location=(dim_x_int / 2 + espesor_muro / 2, 0, altura_int / 2),
    scale=(espesor_muro, dim_y_int, altura_int)
)

# Crear Muro Oeste (-X)
bpy.ops.mesh.primitive_cube_add(
    location=(-dim_x_int / 2 - espesor_muro / 2, 0, altura_int / 2),
    scale=(espesor_muro, dim_y_int, altura_int)
)