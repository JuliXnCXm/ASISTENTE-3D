import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
largo = 2.2
profundidad = 0.9
altura_total = 0.8
altura_base = 0.4

# Crear la base del sofá
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo / 2, profundidad / 2, altura_base / 2),
    scale=(largo, profundidad, altura_base)
)
bpy.context.active_object.name = "SofaBase"

# Crear el respaldo del sofá
altura_respaldo = altura_total - altura_base
espesor_respaldo = 0.2
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo / 2, espesor_respaldo / 2, altura_base + altura_respaldo / 2),
    scale=(largo, espesor_respaldo, altura_respaldo)
)
bpy.context.active_object.name = "SofaRespaldo"