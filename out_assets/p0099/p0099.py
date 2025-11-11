import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones de la alfombra
diametro = 3.0
grosor = 0.02
radio = diametro / 2

# Crear la alfombra usando un cilindro
bpy.ops.mesh.primitive_cylinder_add(
    vertices=128,  # Para una apariencia suave
    radius=radio,
    depth=grosor,
    location=(0, 0, grosor / 2) # Apoyada en el suelo
)

# Renombrar el objeto
alfombra = bpy.context.active_object
alfombra.name = 'AlfombraCircular'