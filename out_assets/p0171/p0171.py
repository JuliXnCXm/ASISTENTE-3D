import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones del muro
largo = 10.0
alto = 2.5
espesor = 0.3

# Crear el muro usando un cubo
bpy.ops.mesh.primitive_cube_add(size=1, location=(largo / 2, espesor / 2, alto / 2))
muro = bpy.context.active_object
muro.name = "MuroContencion"

# Escalar el objeto a las dimensiones deseadas
muro.scale = (largo, espesor, alto)

# Aplicar la escala
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)