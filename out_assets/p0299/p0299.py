import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones del muro
largo = 10.0
alto = 2.5
espesor = 0.2

# Crear el muro usando un cubo
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(espesor / 2, largo / 2, alto / 2), 
    scale=(espesor, largo, alto)
)

muro = bpy.context.active_object
muro.name = 'MuroCerramiento'