import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones del muro
largo = 5.0
alto = 2.5
espesor = 0.15

# Crear el muro usando un cubo
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo / 2, espesor / 2, alto / 2),
    scale=(largo, espesor, alto)
)

# Renombrar el objeto
muro = bpy.context.active_object
muro.name = 'MuroParticion'