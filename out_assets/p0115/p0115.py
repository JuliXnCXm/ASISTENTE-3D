import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo = 2.2
ancho_total = 1.0
alto_total = 0.9
voladizo = 0.3
espesor_encimera = 0.04

# Calcular dimensiones del cuerpo y la encimera
ancho_cuerpo = ancho_total - voladizo
alto_cuerpo = alto_total - espesor_encimera

# Crear el cuerpo de la isla
loc_y_cuerpo = voladizo / 2
loc_z_cuerpo = alto_cuerpo / 2
bpy.ops.mesh.primitive_cube_add(
    location=(0, loc_y_cuerpo, loc_z_cuerpo),
    scale=(largo, ancho_cuerpo, alto_cuerpo)
)

# Crear la encimera
loc_z_encimera = alto_cuerpo + espesor_encimera / 2
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, loc_z_encimera),
    scale=(largo, ancho_total, espesor_encimera)
)