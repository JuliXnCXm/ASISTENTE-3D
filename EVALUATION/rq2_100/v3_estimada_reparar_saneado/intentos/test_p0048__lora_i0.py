import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del techo ---
ancho_total = 6.0
profundidad_total = 4.0
alto_suspension = 2.8
tamano_panel = 1.0
ancho_perfil = 0.05
num_paneles_x = int(ancho_total / tamano_panel)
num_paneles_y = int(profundidad_total / tamano_panel)

# --- Creación de paneles ---
for i in range(num_paneles_x):
    for j in range(num_paneles_y):
        pos_x = -ancho_total/2 + i * tamano_panel + tamano_panel/2
        pos_y = -profundidad_total/2 + j * tamano_panel + tamano_panel/2
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=(pos_x, pos_y, alto_suspension),
            scale=(tamano_panel, tamano_panel, tamano_panel)
        )
        bpy.context.object.name = f"Panel_{i}_{j}"

# --- Creación de perfiles verticales ---
for i in range(num_paneles_x + 1):
    pos_x = -ancho_total/2 + i * tamano_panel
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, -profundidad_total/2, alto_suspension + tamano_panel/2),
        scale=(ancho_perfil, profundidad_total, tamano_panel)
    )
    bpy.context.object.name = f"Perfil_Vertical_{i}"

# --- Creación de perfiles horizontales ---
for j in range(num_paneles_y + 1):
    pos_y = -profundidad_total/2 + j * tamano_panel
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(-ancho_total/2, pos_y, alto_suspension + tamano_panel/2),
        scale=(ancho_total + ancho_perfil, ancho_perfil, tamano_panel)
    )
    bpy.context.object.name = f"Perfil_Horizontal_{j}"

# --- Añadir iluminación ---
bpy.ops.object.light_add(
    type='POINT',
    radius=1.0,
    location=(-2, 2, 3)
)
bpy.context.object.data.energy = 150

bpy.ops.object.light_add(
    type='POINT',
    radius=1.0,
    location=(2, -2, 3)
)
bpy.context.object.data.energy = 150

bpy.ops.object.light_add(
    type='POINT',
    radius=1.0,
    location=(-2, -2, 3)
)
bpy.context.object.data.energy = 150

bpy.ops.object.light_add(
    type='POINT',
    radius=1.0,
    location=(2, 2, 3)
)
bpy.context.object.data.energy = 150