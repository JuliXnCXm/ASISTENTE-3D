import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la pérgola ---
ancho = 4.0
fondo = 3.0
alto = 2.5
seccion_poste = 0.2
seccion_viga = (0.15, 0.2)
seccion_vigueta = (0.08, 0.1)

# --- Crear Postes ---
posiciones_postes = [
    (-ancho/2, -fondo/2), (ancho/2, -fondo/2),
    (-ancho/2, fondo/2), (ancho/2, fondo/2)
]
for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos[0], pos[1], alto/2),
        scale=(seccion_poste, seccion_poste, alto)
    )
    bpy.context.object.name = f"Poste_{i+1}"

# --- Crear Vigas Principales ---
# Viga 1 (a lo largo de X)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, -fondo/2, alto + seccion_viga[1]/2),
    scale=(ancho + seccion_poste, seccion_viga[1], seccion_viga[0])
)
bpy.context.object.name = "Viga_Principal_1"

# Viga 2 (a lo largo de Y)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-ancho/2, 0, alto + seccion_viga[1]/2),
    scale=(seccion_viga[0], fondo + seccion_poste, seccion_viga[0])
)
bpy.context.object.name = "Viga_Principal_2"

# --- Crear Emparrillado Superior ---
num_viguetas = 7
espaciado = ancho / (num_viguetas - 1) if num_viguetas > 1 else 0

for i in range(num_viguetas):
    x_pos = -ancho/2 + i * espaciado
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x_pos, 0, alto + seccion_viga[1] + seccion_vigueta[1]/2),
        scale=(seccion_vigueta[0], fondo + seccion_poste, seccion_vigueta[1])
    )
    bpy.context.object.name = f"Vigueta_{i+1}"