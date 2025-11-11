import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones del muro
largo = 8.0
alto = 2.5
espesor = 0.3

# Crear el muro (un cubo escalado)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(largo / 2, 0, alto / 2)
)

# Ajustar dimensiones del objeto recién creado
muro = bpy.context.active_object
muro.name = 'MuroLadrillo'
muro.dimensions = (largo, espesor, alto)