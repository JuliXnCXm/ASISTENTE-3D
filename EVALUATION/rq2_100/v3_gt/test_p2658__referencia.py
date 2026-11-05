import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

ancho_total = 1.2
alto_total = 2.0
profundidad = 0.3
espesor_panel = 0.02
num_estantes = 5

# Paneles verticales
ancho_interno = ancho_total - 2 * espesor_panel
alto_interno = alto_total - 2 * espesor_panel

bpy.ops.mesh.primitive_cube_add(location=(ancho_total / 2 - espesor_panel / 2, profundidad / 2, alto_total / 2), scale=(espesor_panel, profundidad, alto_total))
bpy.ops.mesh.primitive_cube_add(location=(-ancho_total / 2 + espesor_panel / 2, profundidad / 2, alto_total / 2), scale=(espesor_panel, profundidad, alto_total))

# Panel superior e inferior
bpy.ops.mesh.primitive_cube_add(location=(0, profundidad / 2, alto_total - espesor_panel / 2), scale=(ancho_interno, profundidad, espesor_panel))
bpy.ops.mesh.primitive_cube_add(location=(0, profundidad / 2, espesor_panel / 2), scale=(ancho_interno, profundidad, espesor_panel))

# Estantes interiores
espacio_entre_estantes = alto_interno / (num_estantes - 1)

for i in range(1, num_estantes - 1):
    altura_estante = espesor_panel + i * espacio_entre_estantes
    bpy.ops.mesh.primitive_cube_add(location=(0, profundidad / 2, altura_estante), scale=(ancho_interno, profundidad, espesor_panel))

# Unir todo
bpy.ops.object.select_all(action='SELECT')
bpy.context.view_layer.objects.active = bpy.data.objects[0]
bpy.ops.object.join()
estanteria = bpy.context.active_object
estanteria.name = 'Estanteria'

for obj in bpy.context.selected_objects:
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)