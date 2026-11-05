import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
ancho_pergola = 4.0
profundidad_pergola = 3.0
altura_pergola = 2.8
dimension_poste = 0.15
alto_viga = 0.2
espesor_vigueta = 0.08
num_viguetas = 7

# Crear Postes
for i in [-1, 1]:
    for j in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(
                i * (ancho_pergola / 2 - dimension_poste / 2),
                j * (profundidad_pergola / 2 - dimension_poste / 2),
                altura_pergola / 2
            ),
            scale=(dimension_poste, dimension_poste, altura_pergola)
        )
        bpy.context.object.name = f'Poste_{i}_{j}'

# Crear Vigas principales (a lo largo de la profundidad)
for i in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(
            i * (ancho_pergola / 2 - dimension_poste / 2),
            0,
            altura_pergola + alto_viga / 2
        ),
        scale=(dimension_poste, profundidad_pergola, alto_viga)
    )
    bpy.context.object.name = f'Viga_Principal_{i}'

# Crear Viguetas transversales (a lo largo del ancho)
espaciado_viguetas = profundidad_pergola / (num_viguetas - 1)
for i in range(num_viguetas):
    pos_y = -profundidad_pergola / 2 + i * espaciado_viguetas
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(
            0,
            pos_y,
            altura_pergola + alto_viga + espesor_vigueta / 2
        ),
        scale=(ancho_pergola, espesor_vigueta, espesor_vigueta * 1.5)
    )
    bpy.context.object.name = f'Vigueta_{i}'

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)