import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# --- Configuración de la escena
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros
dimension_base = 3.0
altura_poste = 2.5
lado_poste = 0.15
ancho_viga = 0.15
alto_viga = 0.20
num_travesanos = 5

# --- Crear Postes
posiciones_postes = [
    (0, 0), (dimension_base - lado_poste, 0), 
    (0, dimension_base - lado_poste), 
    (dimension_base - lado_poste, dimension_base - lado_poste)
]
for i, pos in enumerate(posiciones_postes):
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos[0] + lado_poste/2, pos[1] + lado_poste/2, altura_poste/2)
    )
    poste = bpy.context.active_object
    poste.name = f"Poste_{i+1}"
    poste.dimensions = (lado_poste, lado_poste, altura_poste)
    bpy.ops.object.transform_apply(scale=True)

# --- Crear Vigas Principales
for i in range(2):
    pos_y = i * (dimension_base - ancho_viga)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=((dimension_base - lado_poste)/2, pos_y + ancho_viga/2, altura_poste + alto_viga/2)
    )
    viga = bpy.context.active_object
    viga.name = f"VigaPrincipal_{i+1}"
    viga.dimensions = (dimension_base, ancho_viga, alto_viga)
    bpy.ops.object.transform_apply(scale=True)

# --- Crear Travesaños
espaciado = (dimension_base - ancho_viga) / (num_travesanos - 1)
for i in range(num_travesanos):
    pos_x = i * espaciado
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x + ancho_viga/2, (dimension_base-lado_poste)/2, altura_poste + alto_viga*1.5)
    )
    travesano = bpy.context.active_object
    travesano.name = f"Travesano_{i+1}"
    travesano.dimensions = (ancho_viga, dimension_base, ancho_viga) # Ancho y alto intercambiados
    bpy.ops.object.transform_apply(scale=True)