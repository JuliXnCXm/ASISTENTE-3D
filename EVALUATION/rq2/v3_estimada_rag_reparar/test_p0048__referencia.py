import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
largo_sala = 6.0
ancho_sala = 4.0
altura_techo = 2.8
ancho_perfil = 0.05
tamano_panel = 1.0
grosor_panel = 0.01
alto_perfil = 0.04

# --- Creación de la retícula de perfiles ---
num_paneles_x = int(largo_sala / tamano_panel)
num_paneles_y = int(ancho_sala / tamano_panel)

# Perfiles longitudinales (dirección X)
for i in range(num_paneles_y + 1):
    pos_y = i * tamano_panel
    bpy.ops.mesh.primitive_cube_add(
        location=(largo_sala / 2, pos_y, altura_techo + alto_perfil/2),
        scale=(largo_sala, ancho_perfil, alto_perfil)
    )
    bpy.context.object.name = f'Perfil_Long_{i}'

# Perfiles transversales (dirección Y)
for i in range(num_paneles_x + 1):
    pos_x = i * tamano_panel
    bpy.ops.mesh.primitive_cube_add(
        location=(pos_x, ancho_sala / 2, altura_techo + alto_perfil/2),
        scale=(ancho_perfil, ancho_sala, alto_perfil)
    )
    bpy.context.object.name = f'Perfil_Trans_{i}'

# --- Creación de los paneles ---
for i in range(num_paneles_x):
    for j in range(num_paneles_y):
        pos_x = i * tamano_panel + tamano_panel / 2
        pos_y = j * tamano_panel + tamano_panel / 2
        bpy.ops.mesh.primitive_cube_add(
            location=(pos_x, pos_y, altura_techo + grosor_panel/2),
            scale=(tamano_panel - ancho_perfil, tamano_panel - ancho_perfil, grosor_panel)
        )
        bpy.context.object.name = f'Panel_{i}_{j}'

# --- Creación de Focos (Spotlights) ---
focos_pos = [(1.5, 1.5), (4.5, 1.5), (1.5, 2.5), (4.5, 2.5)]
for i, pos in enumerate(focos_pos):
    bpy.ops.object.light_add(
        type='SPOT',
        location=(pos[0], pos[1], altura_techo - 0.1),
        rotation=(0, 0, 0)
    )
    light = bpy.context.object
    light.data.energy = 80 # Watts
    light.data.spot_size = 1.2 # Radianes
    light.name = f'Foco_{i+1}'