import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo = 4.0 # X
ancho = 3.0 # Y
alto = 2.5
grosor_poste = 0.15
alto_viga = 0.2
grosor_viga = 0.1
alto_vigueta = 0.15
grosor_vigueta = 0.08
num_viguetas = 5

# Crear Postes
pos_x_poste = (largo - grosor_poste) / 2
pos_y_poste = (ancho - grosor_poste) / 2
locs_postes = [
    (pos_x_poste, pos_y_poste, alto/2),
    (-pos_x_poste, pos_y_poste, alto/2),
    (pos_x_poste, -pos_y_poste, alto/2),
    (-pos_x_poste, -pos_y_poste, alto/2)
]
for i, loc in enumerate(locs_postes):
    bpy.ops.mesh.primitive_cube_add(location=loc, scale=(grosor_poste, grosor_poste, alto))
    bpy.context.object.name = f'Poste_{i}'

# Crear Vigas Principales (a lo largo de X)
pos_y_viga = (ancho - grosor_viga) / 2
bpy.ops.mesh.primitive_cube_add(location=(0, pos_y_viga, alto + alto_viga/2), scale=(largo, grosor_viga, alto_viga))
bpy.context.object.name = 'Viga_1'
bpy.ops.mesh.primitive_cube_add(location=(0, -pos_y_viga, alto + alto_viga/2), scale=(largo, grosor_viga, alto_viga))
bpy.context.object.name = 'Viga_2'

# Crear Viguetas Transversales (a lo largo de Y)
espacio_viguetas = largo / (num_viguetas - 1)
for i in range(num_viguetas):
    pos_x_vigueta = -largo/2 + i * espacio_viguetas
    bpy.ops.mesh.primitive_cube_add(
        location=(pos_x_vigueta, 0, alto + alto_viga + alto_vigueta/2),
        scale=(grosor_vigueta, ancho, alto_vigueta)
    )
    bpy.context.object.name = f'Vigueta_{i}'