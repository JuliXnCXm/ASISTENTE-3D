import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)

# Configuración de escena
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo_pergola = 4.0
ancho_pergola = 3.0
altura_pergola = 2.5
seccion_poste = 0.15
seccion_viga = (0.1, 0.2)
seccion_vigueta = (0.08, 0.15)
separacion_viguetas = 0.5

# Crear Postes
posiciones_postes = [
    (-largo_pergola / 2, -ancho_pergola / 2),
    (largo_pergola / 2, -ancho_pergola / 2),
    (-largo_pergola / 2, ancho_pergola / 2),
    (largo_pergola / 2, ancho_pergola / 2)
]
for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(
        location=(pos[0], pos[1], altura_pergola / 2),
        scale=(seccion_poste / 2, seccion_poste / 2, altura_pergola / 2)
    )
    bpy.context.object.name = f"Poste_{i+1}"

# Crear Vigas Principales (a lo largo de X)
posiciones_vigas = [-ancho_pergola / 2, ancho_pergola / 2]
for i, pos_y in enumerate(posiciones_vigas):
    bpy.ops.mesh.primitive_cube_add(
        location=(0, pos_y, altura_pergola + seccion_viga[1] / 2),
        scale=((largo_pergola + seccion_poste) / 2, seccion_viga[0] / 2, seccion_viga[1] / 2)
    )
    bpy.context.object.name = f"VigaPrincipal_{i+1}"

# Crear Viguetas Transversales (a lo largo de Y)
num_viguetas = int(largo_pergola / separacion_viguetas) + 1
for i in range(num_viguetas):
    pos_x = -largo_pergola / 2 + i * separacion_viguetas
    bpy.ops.mesh.primitive_cube_add(
        location=(pos_x, 0, altura_pergola + seccion_viga[1] + seccion_vigueta[1] / 2),
        scale=(seccion_vigueta[0] / 2, (ancho_pergola + seccion_poste) / 2, seccion_vigueta[1] / 2)
    )
    bpy.context.object.name = f"Vigueta_{i+1}"