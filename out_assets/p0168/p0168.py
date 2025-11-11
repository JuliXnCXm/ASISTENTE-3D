import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_x = 4.0
ancho_y = 3.0
alto_z = 2.5
seccion_poste = 0.15
seccion_viga_principal = (0.1, 0.2)
seccion_viga_secundaria = (0.08, 0.15)
num_vigas_secundarias = 7

# Crear un objeto Empty para agrupar la pérgola
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
pergola_parent = bpy.context.active_object
pergola_parent.name = 'Pergola'

# Crear 4 postes
posiciones_postes = [
    (largo_x / 2, ancho_y / 2, alto_z / 2),
    (-largo_x / 2, ancho_y / 2, alto_z / 2),
    (-largo_x / 2, -ancho_y / 2, alto_z / 2),
    (largo_x / 2, -ancho_y / 2, alto_z / 2)
]

for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(
        location=pos,
        scale=(seccion_poste / 2, seccion_poste / 2, alto_z / 2)
    )
    poste = bpy.context.active_object
    poste.name = f'Poste_{i+1}'
    poste.parent = pergola_parent

# Crear 2 vigas principales (eje X)
for i, y_pos in enumerate([-ancho_y / 2, ancho_y / 2]):
    bpy.ops.mesh.primitive_cube_add(
        location=(0, y_pos, alto_z + seccion_viga_principal[1] / 2),
        scale=(largo_x / 2, seccion_viga_principal[0] / 2, seccion_viga_principal[1] / 2)
    )
    viga_p = bpy.context.active_object
    viga_p.name = f'VigaPrincipal_{i+1}'
    viga_p.parent = pergola_parent

# Crear vigas secundarias (emparrillado eje Y)
espaciado = largo_x / (num_vigas_secundarias - 1)
for i in range(num_vigas_secundarias):
    x_pos = -largo_x / 2 + i * espaciado
    bpy.ops.mesh.primitive_cube_add(
        location=(x_pos, 0, alto_z + seccion_viga_principal[1] + seccion_viga_secundaria[1] / 2),
        scale=(seccion_viga_secundaria[0] / 2, ancho_y / 2, seccion_viga_secundaria[1] / 2)
    )
    viga_s = bpy.context.active_object
    viga_s.name = f'VigaSecundaria_{i+1}'
    viga_s.parent = pergola_parent