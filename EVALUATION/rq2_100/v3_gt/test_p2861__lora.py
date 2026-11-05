import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la pérgola ---
ancho = 4.0
fondo = 3.0
alto = 2.8
seccion_poste = 0.15
seccion_vigueta = (0.10, 0.15)

# --- Crear Postes ---
posiciones_postes = [
    (-ancho/2, -fondo/2),
    (ancho/2, -fondo/2),
    (-ancho/2, fondo/2),
    (ancho/2, fondo/2)
]

for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos[0], pos[1], alto/2),
        scale=(seccion_poste, seccion_poste, alto)
    )
    bpy.context.object.name = f"Poste_{i+1}"

# --- Crear Viguetas Principales (a lo largo) ---
num_viguetas_principales = 6
espaciado_viguetas = ancho / (num_viguetas_principales - 1)

for i in range(num_viguetas_principales):
    x_pos = -ancho/2 + i * espaciado_viguetas
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x_pos, 0, alto + seccion_vigueta[1]/2),
        scale=(seccion_vigueta[0], fondo + seccion_poste, seccion_vigueta[1])
    )
    bpy.context.object.name = f"Vigueta_Larga_{i+1}"

# --- Crear Viguetas Secundarias (a lo ancho) ---
num_viguetas_secundarias = 7
espaciado_viguetas_secundarias = fondo / (num_viguetas_secundarias - 1)

for i in range(num_viguetas_secundarias):
    z_pos = alto + seccion_vigueta[1] + i * espaciado_viguetas_secundarias
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, i * espaciado_viguetas_secundarias, z_pos),
        scale=(ancho + seccion_poste, seccion_vigueta[0], seccion_vigueta[1])
    )
    bpy.context.object.name = f"Vigueta_Corta_{i+1}"