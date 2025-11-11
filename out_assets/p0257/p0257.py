import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
largo = 4.0
ancho = 3.0
altura = 2.5
tamano_poste = 0.15
alto_viga = 0.2
ancho_viga = 0.1
num_vigas_transversales = 7

# --- Creación de los 4 postes ---
posiciones_postes = [
    (largo / 2, ancho / 2, altura / 2),
    (-largo / 2, ancho / 2, altura / 2),
    (largo / 2, -ancho / 2, altura / 2),
    (-largo / 2, -ancho / 2, altura / 2)
]
for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(location=pos)
    poste = bpy.context.active_object
    poste.name = f"Pergola.Poste_{i+1}"
    poste.dimensions = (tamano_poste, tamano_poste, altura)

# --- Creación de vigas principales (largas) ---
pos_y_vigas = [ancho / 2, -ancho / 2]
for i, pos_y in enumerate(pos_y_vigas):
    bpy.ops.mesh.primitive_cube_add(location=(0, pos_y, altura + alto_viga / 2))
    viga = bpy.context.active_object
    viga.name = f"Pergola.VigaPrincipal_{i+1}"
    viga.dimensions = (largo + tamano_poste, ancho_viga, alto_viga)

# --- Creación de vigas transversales (cortas) ---
espaciado = largo / (num_vigas_transversales - 1)
for i in range(num_vigas_transversales):
    pos_x = -largo / 2 + i * espaciado
    bpy.ops.mesh.primitive_cube_add(location=(pos_x, 0, altura + alto_viga + ancho_viga / 2))
    viga_t = bpy.context.active_object
    viga_t.name = f"Pergola.VigaTransversal_{i+1}"
    viga_t.dimensions = (ancho_viga, ancho + tamano_poste, alto_viga)