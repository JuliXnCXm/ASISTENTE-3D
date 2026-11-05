import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
dim_x, dim_y, altura = 4.0, 3.0, 2.8
sec_poste = 0.15
sec_viga_x, sec_viga_y = 0.15, 0.20
sec_vigueta_x, sec_vigueta_y = 0.1, 0.15
num_viguetas = 5

# Crear Postes
posiciones_postes = [
    (dim_x/2 - sec_poste/2, dim_y/2 - sec_poste/2),
    (-dim_x/2 + sec_poste/2, dim_y/2 - sec_poste/2),
    (dim_x/2 - sec_poste/2, -dim_y/2 + sec_poste/2),
    (-dim_x/2 + sec_poste/2, -dim_y/2 + sec_poste/2)
]
for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos[0], pos[1], altura/2),
        scale=(sec_poste, sec_poste, altura)
    )
    bpy.context.active_object.name = f'Poste_{i+1}'

# Crear Vigas Principales (a lo largo de X)
for i, y_pos in enumerate([-dim_y/2 + sec_poste/2, dim_y/2 - sec_poste/2]):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, y_pos, altura + sec_viga_y/2),
        scale=(dim_x, sec_viga_x, sec_viga_y)
    )
    bpy.context.active_object.name = f'Viga_Principal_{i+1}'

# Crear Viguetas Transversales (a lo largo de Y)
separacion = (dim_x - sec_vigueta_x) / (num_viguetas - 1)
for i in range(num_viguetas):
    x_pos = -dim_x/2 + sec_vigueta_x/2 + i * separacion
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x_pos, 0, altura + sec_viga_y + sec_vigueta_y/2),
        scale=(sec_vigueta_x, dim_y, sec_vigueta_y)
    )
    bpy.context.active_object.name = f'Vigueta_{i+1}'