import bpy

# Configuración inicial
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
losa_largo = 15.0
losa_ancho = 3.0
losa_espesor = 0.15
bordillo_ancho = 0.2
bordillo_alto = 0.1

# Crear la losa de la acera
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, -losa_espesor / 2)
)
losa = bpy.context.active_object
losa.name = "LosaAcera"
losa.dimensions = (losa_largo, losa_ancho, losa_espesor)

# Crear el bordillo
pos_y_bordillo = losa_ancho / 2 - bordillo_ancho / 2
pos_z_bordillo = bordillo_alto / 2
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, pos_y_bordillo, pos_z_bordillo)
)
bordillo = bpy.context.active_object
bordillo.name = "Bordillo"
bordillo.dimensions = (losa_largo, bordillo_ancho, bordillo_alto)