import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho_x = 4.0
profundo_y = 3.0
alto_z = 2.5
tamano_poste = 0.15
ancho_viga = 0.1
alto_viga = 0.2
ancho_vigueta = 0.08
alto_vigueta = 0.15
num_viguetas = 5

# Crear un objeto vacío como padre
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
pergola_parent = bpy.context.active_object
pergola_parent.name = "Pergola"

# Crear 4 postes
posiciones_postes = [
    (-ancho_x / 2, -profundo_y / 2),
    ( ancho_x / 2, -profundo_y / 2),
    ( ancho_x / 2,  profundo_y / 2),
    (-ancho_x / 2,  profundo_y / 2)
]
for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos[0], pos[1], alto_z / 2),
        scale=(tamano_poste / 2, tamano_poste / 2, alto_z / 2)
    )
    poste = bpy.context.active_object
    poste.name = f"Poste.{i+1:03d}"
    poste.parent = pergola_parent

# Crear 2 vigas principales (a lo largo de X)
posiciones_vigas = [-profundo_y / 2, profundo_y / 2]
for i, pos_y in enumerate(posiciones_vigas):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, pos_y, alto_z + alto_viga / 2),
        scale=(ancho_x / 2, ancho_viga / 2, alto_viga / 2)
    )
    viga = bpy.context.active_object
    viga.name = f"VigaPrincipal.{i+1:03d}"
    viga.parent = pergola_parent

# Crear 5 viguetas (a lo largo de Y)
espaciado_viguetas = ancho_x / (num_viguetas - 1)
for i in range(num_viguetas):
    pos_x = -ancho_x / 2 + i * espaciado_viguetas
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, alto_z + alto_viga + alto_vigueta / 2),
        scale=(ancho_vigueta / 2, profundo_y / 2, alto_vigueta / 2)
    )
    vigueta = bpy.context.active_object
    vigueta.name = f"Vigueta.{i+1:03d}"
    vigueta.parent = pergola_parent