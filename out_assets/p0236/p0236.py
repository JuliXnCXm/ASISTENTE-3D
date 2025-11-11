import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_pergola = 4.0
ancho_pergola = 3.0
alto_pergola = 2.8
dim_poste = 0.2
alto_viga = 0.2
ancho_viga = 0.15

# Crear postes
posiciones_postes = [
    (0, 0), (largo_pergola, 0), 
    (0, ancho_pergola), (largo_pergola, ancho_pergola)
]
for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos[0], pos[1], alto_pergola / 2),
        scale=(dim_poste, dim_poste, alto_pergola)
    )
    bpy.context.active_object.name = f"Poste_{i+1}"

# Crear vigas principales (dirección Y)
for x_pos in [0, largo_pergola]:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x_pos, ancho_pergola / 2, alto_pergola + alto_viga / 2),
        scale=(dim_poste, ancho_pergola, alto_viga)
    )
    bpy.context.active_object.name = f"VigaPrincipal_{'Izq' if x_pos==0 else 'Der'}"

# Crear viguetas (dirección X)
num_viguetas = 7
espaciado = largo_pergola / (num_viguetas - 1)
for i in range(num_viguetas):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(i * espaciado, ancho_pergola / 2, alto_pergola + alto_viga / 2),
        scale=(ancho_viga, ancho_pergola, alto_viga)
    )
    bpy.context.active_object.name = f"Vigueta_{i+1}"