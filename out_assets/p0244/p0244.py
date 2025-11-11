import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo = 2.5
ancho = 0.6
alto = 0.8
grosor = 0.05

# Crear postes
pos_x = (largo - grosor) / 2
pos_y = (ancho - grosor) / 2

locations = [
    (pos_x, pos_y, alto / 2),
    (-pos_x, pos_y, alto / 2),
    (pos_x, -pos_y, alto / 2),
    (-pos_x, -pos_y, alto / 2)
]

for i, loc in enumerate(locations):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=loc,
        scale=(grosor, grosor, alto)
    )
    bpy.context.object.name = f'Poste_{i+1}'

# Crear paneles
largo_panel_largo = largo - grosor * 2
largo_panel_ancho = ancho - grosor * 2

# Paneles largos (eje X)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, pos_y, alto / 2), scale=(largo_panel_largo, grosor, alto))
bpy.context.object.name = 'Panel_Largo_1'
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -pos_y, alto / 2), scale=(largo_panel_largo, grosor, alto))
bpy.context.object.name = 'Panel_Largo_2'

# Paneles anchos (eje Y)
bpy.ops.mesh.primitive_cube_add(size=1, location=(pos_x, 0, alto / 2), scale=(grosor, largo_panel_ancho, alto))
bpy.context.object.name = 'Panel_Ancho_1'
bpy.ops.mesh.primitive_cube_add(size=1, location=(-pos_x, 0, alto / 2), scale=(grosor, largo_panel_ancho, alto))
bpy.context.object.name = 'Panel_Ancho_2'