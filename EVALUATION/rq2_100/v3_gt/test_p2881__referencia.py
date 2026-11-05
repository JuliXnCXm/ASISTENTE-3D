import bpy

# --- Configuración de la Escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# --- Dimensiones ---
ancho_fachada = 8.0
alto_fachada = 6.0
espesor_muro = 0.2
altura_piso = 3.0

ancho_balcon = 3.0
prof_balcon = 1.2
espesor_losa = 0.15

# --- Crear Muro de Fachada ---
bpy.ops.mesh.primitive_cube_add(
    location=(0, espesor_muro / 2, alto_fachada / 2),
    scale=(ancho_fachada, espesor_muro, alto_fachada)
)
muro = bpy.context.active_object
muro.name = 'Muro_Fachada'

# --- Crear Losa de Balcón ---
bpy.ops.mesh.primitive_cube_add(
    location=(0, espesor_muro + prof_balcon / 2, altura_piso - espesor_losa / 2),
    scale=(ancho_balcon, prof_balcon, espesor_losa)
)
losa_balcon = bpy.context.active_object
losa_balcon.name = 'Losa_Balcon'

# --- Crear Barandilla ---
alto_barandilla = 1.0
diam_poste = 0.05

# Posiciones de los postes
posiciones = [
    (ancho_balcon / 2 - diam_poste, espesor_muro + diam_poste, altura_piso),
    (ancho_balcon / 2 - diam_poste, espesor_muro + prof_balcon - diam_poste, altura_piso),
    (-ancho_balcon / 2 + diam_poste, espesor_muro + prof_balcon - diam_poste, altura_piso),
    (-ancho_balcon / 2 + diam_poste, espesor_muro + diam_poste, altura_piso)
]

for i, pos in enumerate(posiciones):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=diam_poste / 2,
        depth=alto_barandilla,
        location=(pos[0], pos[1], pos[2] + alto_barandilla / 2)
    )
    bpy.context.object.name = f'Poste_{i+1}'

# Pasamanos frontal
bpy.ops.mesh.primitive_cube_add(
    location=(0, espesor_muro + prof_balcon - diam_poste, altura_piso + alto_barandilla),
    scale=(ancho_balcon, diam_poste, diam_poste)
)
bpy.context.object.name = 'Pasamanos_Frontal'

# Pasamanos lateral derecho
bpy.ops.mesh.primitive_cube_add(
    location=(ancho_balcon / 2 - diam_poste, espesor_muro + prof_balcon/2, altura_piso + alto_barandilla),
    scale=(diam_poste, prof_balcon, diam_poste)
)
bpy.context.object.name = 'Pasamanos_Derecho'

# Pasamanos lateral izquierdo
bpy.ops.mesh.primitive_cube_add(
    location=(-ancho_balcon / 2 + diam_poste, espesor_muro + prof_balcon/2, altura_piso + alto_barandilla),
    scale=(diam_poste, prof_balcon, diam_poste)
)
bpy.context.object.name = 'Pasamanos_Izquierdo'