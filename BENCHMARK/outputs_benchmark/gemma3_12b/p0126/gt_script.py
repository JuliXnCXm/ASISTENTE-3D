import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones del muro
largo = 4.0
alto = 2.5
espesor = 0.15

# Crear el muro (cubo escalado)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo / 2, 0, alto / 2),
    scale=(largo, espesor, alto)
)

muro = bpy.context.object
muro.name = "MuroParticion"