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

# --- Crear Viguetas Principales (a lo largo) ---
num_viguetas_largas = int(ancho / seccion_vigueta[0]) + 1
espaciado_largo = ancho / num_viguetas_largas

for i in range(num_viguetas_largas):
    x_pos = -ancho/2 + espaciado_largo * i
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x_pos, 0, alto + seccion_vigueta[1]/2),
        scale=(seccion_vigueta[0], fondo + seccion_poste*2, seccion_vigueta[1])
    )
    bpy.context.object.name = f"Vigueta_Larga_{i+1}"

# --- Crear Viguetas Secundarias (a lo ancho) ---
num_viguetas_cortas = int(fondo / seccion_vigueta[0]) + 1
espaciado_corto = fondo / num_viguetas_cortas

for i in range(num_viguetas_cortas):
    z_pos = alto + seccion_vigueta[1]/2 + espaciado_corto * i
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, -fondo/2 + espaciado_corto * i, z_pos),
        scale=(ancho + seccion_poste*2, seccion_vigueta[0], seccion_vigueta[1])
    )
    bpy.context.object.name = f"Vigueta_Corta_{i+1}"