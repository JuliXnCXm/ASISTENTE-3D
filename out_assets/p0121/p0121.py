import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la isla ---
largo = 2.2
ancho_total = 0.9
alto_total = 0.9
espesor_encimera = 0.04
voladizo = 0.3

# --- Dimensiones de los componentes ---
ancho_base = ancho_total - voladizo
alto_base = alto_total - espesor_encimera

# --- Creación de la base ---
escala_base = (largo, ancho_base, alto_base)
loc_base = (0, -voladizo / 2, alto_base / 2)
bpy.ops.mesh.primitive_cube_add(size=1, scale=escala_base, location=loc_base)
base = bpy.context.active_object
base.name = "BaseIsla"

# --- Creación de la encimera ---
escala_encimera = (largo, ancho_total, espesor_encimera)
loc_encimera = (0, 0, alto_base + espesor_encimera / 2)
bpy.ops.mesh.primitive_cube_add(size=1, scale=escala_encimera, location=loc_encimera)
encimera = bpy.context.active_object
encimera.name = "EncimeraIsla"