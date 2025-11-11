import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones del muro
largo = 10.0
alto = 2.5
espesor = 0.3

# Creación del muro (usando un cubo escalado)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(largo / 2, espesor / 2, alto / 2)
)
muro = bpy.context.active_object
muro.name = "MuroContencion"
muro.dimensions = (largo, espesor, alto)