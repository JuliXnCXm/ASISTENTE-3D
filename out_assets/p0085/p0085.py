import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
diametro = 2.5
grosor = 0.01
radio = diametro / 2

# Crear la alfombra usando un cilindro
bpy.ops.mesh.primitive_cylinder_add(
    vertices=64, # Para que sea más suave el círculo
    radius=radio,
    depth=grosor,
    enter_editmode=False,
    align='WORLD',
    location=(0, 0, grosor / 2) # Ubicada sobre el origen (piso)
)

alfombra = bpy.context.active_object
alfombra.name = 'AlfombraCircular'