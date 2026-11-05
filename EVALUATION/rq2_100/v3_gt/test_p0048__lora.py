import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del techo ---
ancho_total = 6.0
fondo_total = 4.0
num_paneles_x = 6
num_paneles_y = 4
tamano_panel = 1.0
ancho_perfil = 0.05
altura_suspension = 2.8

# --- Creación de paneles ---
for i in range(num_paneles_x):
    for j in range(num_paneles_y):
        pos_x = -ancho_total / 2 + i * tamano_panel + tamano_panel / 2
        pos_y = -fondo_total / 2 + j * tamano_panel + tamano_panel / 2
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(pos_x, pos_y, altura_suspension),
            scale=(tamano_panel, tamano_panel, 0.01)
        )
        bpy.context.object.name = f"Panel_{i}_{j}"

# --- Creación de perfiles verticales ---
for i in range(num_paneles_x + 1):
    pos_x = -ancho_total / 2 + i * tamano_panel + tamano_panel / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, fondo_total / 2, altura_suspension + tamano_panel / 2),
        scale=(ancho_perfil, fondo_total, tamano_panel)
    )
    bpy.context.object.name = f"Perfil_Vertical_{i}"

# --- Creación de perfiles horizontales ---
for j in range(num_paneles_y + 1):
    pos_y = -fondo_total / 2 + j * tamano_panel + tamano_panel / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(-ancho_total / 2, pos_y, altura_suspension + tamano_panel / 2),
        scale=(ancho_total + ancho_perfil, ancho_perfil, tamano_panel)
    )
    bpy.context.object.name = f"Perfil_Horizontal_{j}"

# --- Añadir iluminación ---
bpy.ops.object.light_add(type='POINT', radius=1, location=(0, 0, altura_suspension + 1.5))
bpy.context.object.data.energy = 150
bpy.context.object.name = "Luz_Techo_1"

bpy.ops.object.light_add(type='POINT', radius=1, location=(-ancho_total / 2, 0, altura_suspension + 1.5))
bpy.context.object.data.energy = 150
bpy.context.object.name = "Luz_Techo_2"

bpy.ops.object.light_add(type='POINT', radius=1, location=(ancho_total / 2, 0, altura_suspension + 1.5))
bpy.context.object.data.energy = 150
bpy.context.object.name = "Luz_Techo_3"

bpy.ops.object.light_add(type='POINT', radius=1, location=(0, fondo_total / 2, altura_suspension + 1.5))
bpy.context.object.data.energy = 150
bpy.context.object.name = "Luz_Techo_4"