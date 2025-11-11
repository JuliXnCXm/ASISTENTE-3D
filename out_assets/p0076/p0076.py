import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
diametro = 3.0
espesor = 0.015

# Crear la alfombra usando un cilindro
bpy.ops.mesh.primitive_cylinder_add(
    vertices=128,
    radius=diametro / 2.0,
    depth=espesor,
    location=(0, 0, espesor / 2.0) # Para que descanse sobre el plano Z=0
)

alfombra = bpy.context.active_object
alfombra.name = 'AlfombraCircular'