import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la pérgola ---
ancho = 4.0
fondo = 3.0
alto_poste = 2.5
dim_poste = 0.2
dim_viga = (0.15, 0.2)
num_viguetas = 7
dim_vigueta = (0.08, 0.1)

# --- Crear Postes ---
posiciones_postes = [
    (-ancho/2, -fondo/2), (ancho/2, -fondo/2),
    (-ancho/2, fondo/2), (ancho/2, fondo/2)
]
for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos[0], pos[1], alto_poste/2),
        scale=(dim_poste, dim_poste, alto_poste)
    )
    bpy.context.object.name = f"Poste_{i+1}"

# --- Crear Vigas Principales ---
pos_y_viga = -fondo/2 + dim_poste/2 + dim_viga[1]/2
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-ancho/2, pos_y_viga, alto_poste + dim_viga[1]/2),
    scale=(ancho, dim_viga[0], dim_viga[1])
)
bpy.context.object.name = "Viga_Principal_1"
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(ancho/2, pos_y_viga, alto_poste + dim_viga[1]/2),
    scale=(ancho, dim_viga[0], dim_viga[1])
)
bpy.context.object.name = "Viga_Principal_2"

# --- Crear Emparrillado Superior ---
espaciado = ancho / (num_viguetas - 1)
for i in range(num_viguetas):
    x_pos = -ancho/2 + i * espaciado
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x_pos, 0, alto_poste + dim_viga[1] + dim_vigueta[1]/2),
        scale=(dim_vigueta[0], fondo, dim_vigueta[1])
    )
    bpy.context.object.name = f"Vigueta_{i+1}"