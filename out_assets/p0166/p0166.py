import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones de las losas y el camino
largo_camino = 5.0
largo_losa = 0.6
ancho_losa = 0.4
espesor_losa = 0.05
separacion = 0.15

# Cálculo del número de losas
longitud_paso = largo_losa + separacion
num_losas = int(largo_camino / longitud_paso)

# Creación de las losas en un bucle
pos_y_actual = 0
for i in range(num_losas):
    bpy.ops.mesh.primitive_cube_add(
        location=(0, pos_y_actual, espesor_losa / 2),
        scale=(ancho_losa / 2, largo_losa / 2, espesor_losa / 2)
    )
    losa = bpy.context.active_object
    losa.name = f'LosaCamino_{i+1:02d}'
    pos_y_actual += longitud_paso