import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

ancho = 0.4
profundidad = 0.4
altura = 2.8

# Crear la columna usando un cubo
bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(0, 0, altura / 2)
)

columna = bpy.context.active_object
columna.name = 'Columna_Cuadrada'

# Asignar dimensiones
columna.dimensions = (ancho, profundidad, altura)

# Aplicar la escala para que las dimensiones sean correctas
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)