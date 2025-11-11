import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
largo_total = 2.0
ancho_total = 0.9
altura_total = 0.9
grosor_encimera = 0.04
voladizo = 0.2

# --- Creación del cuerpo base de la isla ---
altura_base = altura_total - grosor_encimera
ancho_base = ancho_total - voladizo

# La posición en Y se desplaza para dejar espacio al voladizo
pos_y_base = voladizo / 2
bpy.ops.mesh.primitive_cube_add(
    location=(0, pos_y_base, altura_base / 2),
    scale=(largo_total, ancho_base, altura_base)
)
bpy.context.object.name = 'Base_Isla'

# --- Creación de la encimera ---
pos_z_encimera = altura_base + grosor_encimera / 2
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, pos_z_encimera),
    scale=(largo_total, ancho_total, grosor_encimera)
)
bpy.context.object.name = 'Encimera_Isla'