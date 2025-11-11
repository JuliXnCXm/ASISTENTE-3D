import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
largo = 1.2
ancho = 0.4
alto = 0.5
espesor = 0.04

# --- Creación de la base ---
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, espesor / 2),
    scale=(largo, ancho, espesor)
)
bpy.context.object.name = 'Base_Jardinera'

# --- Creación de las paredes ---
altura_pared = alto - espesor

# Pared Larga Frontal
bpy.ops.mesh.primitive_cube_add(
    location=(0, ancho/2 - espesor/2, altura_pared/2 + espesor),
    scale=(largo, espesor, altura_pared)
)
bpy.context.object.name = 'Pared_Frontal'

# Pared Larga Trasera
bpy.ops.mesh.primitive_cube_add(
    location=(0, -ancho/2 + espesor/2, altura_pared/2 + espesor),
    scale=(largo, espesor, altura_pared)
)
bpy.context.object.name = 'Pared_Trasera'

# Pared Corta Izquierda
bpy.ops.mesh.primitive_cube_add(
    location=(-largo/2 + espesor/2, 0, altura_pared/2 + espesor),
    scale=(espesor, ancho - 2*espesor, altura_pared)
)
bpy.context.object.name = 'Pared_Izquierda'

# Pared Corta Derecha
bpy.ops.mesh.primitive_cube_add(
    location=(largo/2 - espesor/2, 0, altura_pared/2 + espesor),
    scale=(espesor, ancho - 2*espesor, altura_pared)
)
bpy.context.object.name = 'Pared_Derecha'