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
dim_viga_principal = (dim_poste, dim_poste, 0.15)
dim_viga_transversal = (dim_poste, dim_poste, 0.1)

# --- Creación de los postes ---
posiciones_postes = [
    (-ancho/2, -fondo/2, alto_poste/2),
    (ancho/2, -fondo/2, alto_poste/2),
    (-ancho/2, fondo/2, alto_poste/2),
    (ancho/2, fondo/2, alto_poste/2)
]

for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(location=pos)
    poste = bpy.context.active_object
    poste.name = f"Poste_{i+1}"
    poste.dimensions = (dim_poste, dim_poste, alto_poste)

# --- Creación de las vigas principales ---
pos_y_vigas_principales = [-fondo/2 + dim_poste/2, fondo/2 - dim_poste/2]
for y_pos in pos_y_vigas_principales:
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, y_pos, alto_poste + dim_viga_principal[2]/2)
    )
    viga = bpy.context.active_object
    viga.name = f"Viga_Principal_{y_pos:.2f}"
    viga.dimensions = (ancho, dim_viga_principal[0], dim_viga_principal[1])

# --- Creación de las vigas transversales ---
num_vigas_transversales = 5
espaciado_vigas = ancho / (num_vigas_transversales - 1) if num_vigas_transversales > 1 else 0
for i in range(num_vigas_transversales):
    x_pos = -ancho/2 + i * espaciado_vigas
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x_pos, 0, alto_poste + dim_viga_transversal[2]/2)
    )
    viga = bpy.context.active_object
    viga.name = f"Viga_Transversal_{i+1}"
    viga.dimensions = (dim_viga_transversal[0], fondo, dim_viga_transversal[1])