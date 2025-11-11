import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
num_estantes = 5
largo = 1.5
profundidad = 0.25
espesor = 0.03
separacion_vertical = 0.35

# Crear los estantes en un bucle
for i in range(num_estantes):
    # La posición Z del centro de cada estante
    pos_z = i * separacion_vertical + espesor / 2
    
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        enter_editmode=False,
        align='WORLD',
        location=(largo / 2, profundidad / 2, pos_z),
        scale=(largo, profundidad, espesor)
    )
    estante = bpy.context.active_object
    estante.name = f"Estante_{i+1:02d}"