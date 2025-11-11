import bpy

bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
L = 4.0
W = 3.0
H = 2.8
seccion_poste = 0.15
seccion_viga = (0.1, 0.2)
seccion_vigueta = (0.08, 0.15)
num_viguetas = 5

# Postes
for i in [-1, 1]:
    for j in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(i * L/2, j * W/2, H/2),
            scale=(seccion_poste, seccion_poste, H)
        )

# Vigas principales (a lo largo de L)
for i in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, i * W/2, H + seccion_viga[1]/2),
        scale=(L + seccion_poste, seccion_viga[0], seccion_viga[1])
    )

# Viguetas transversales (a lo largo de W)
espaciado = L / (num_viguetas - 1) if num_viguetas > 1 else 0
for i in range(num_viguetas):
    pos_x = -L/2 + i * espaciado
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, 0, H + seccion_viga[1] + seccion_vigueta[1]/2),
        scale=(seccion_vigueta[0], W + seccion_poste, seccion_vigueta[1])
    )