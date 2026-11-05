import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
dim_x = 4.0
dim_y = 3.0
altura_postes = 2.5
ancho_poste = 0.2
alto_viga_principal = 0.25
ancho_viga_principal = 0.15
alto_vigueta = 0.15
ancho_vigueta = 0.1
num_viguetas = 7

# Crear Postes
posiciones_postes = [
    (dim_x / 2 - ancho_poste / 2, dim_y / 2 - ancho_poste / 2),
    (-dim_x / 2 + ancho_poste / 2, dim_y / 2 - ancho_poste / 2),
    (dim_x / 2 - ancho_poste / 2, -dim_y / 2 + ancho_poste / 2),
    (-dim_x / 2 + ancho_poste / 2, -dim_y / 2 + ancho_poste / 2)
]

for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(pos[0], pos[1], altura_postes / 2))
    poste = bpy.context.active_object
    poste.name = f'Poste_{i+1}'
    poste.dimensions = (ancho_poste, ancho_poste, altura_postes)

# Crear Vigas Principales
for i in [-1, 1]:
    loc_y = i * (dim_y / 2 - ancho_poste / 2)
    loc_z = altura_postes + alto_viga_principal / 2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, loc_y, loc_z))
    viga = bpy.context.active_object
    viga.name = f'Viga_Principal_{1 if i == -1 else 2}'
    viga.dimensions = (dim_x, ancho_viga_principal, alto_viga_principal)

# Crear Viguetas Transversales
espaciado_viguetas = dim_x / (num_viguetas - 1)
for i in range(num_viguetas):
    loc_x = -dim_x / 2 + i * espaciado_viguetas
    loc_z = altura_postes + alto_viga_principal + alto_vigueta / 2
    bpy.ops.mesh.primitive_cube_add(size=1, location=(loc_x, 0, loc_z))
    vigueta = bpy.context.active_object
    vigueta.name = f'Vigueta_{i+1}'
    vigueta.dimensions = (ancho_vigueta, dim_y + 0.4, alto_vigueta) # Un poco de voladizo