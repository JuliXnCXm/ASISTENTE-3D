import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# --- Configuración de la escena
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros
altura = 3.0
espesor = 0.25
largo_norte = 6.0
largo_oeste = 4.0

# --- Crear Muro Norte (a lo largo del eje X)
bpy.ops.mesh.primitive_cube_add(
    size=1, 
    location=(largo_norte / 2, -espesor / 2, altura / 2)
)
muro_norte = bpy.context.active_object
muro_norte.name = "MuroNorte"
muro_norte.dimensions = (largo_norte, espesor, altura)
bpy.ops.object.transform_apply(scale=True)

# --- Crear Muro Oeste (a lo largo del eje Y)
bpy.ops.mesh.primitive_cube_add(
    size=1, 
    location=(-espesor / 2, largo_oeste / 2 - espesor, altura / 2)
)
muro_oeste = bpy.context.active_object
muro_oeste.name = "MuroOeste"
muro_oeste.dimensions = (espesor, largo_oeste, altura)
bpy.ops.object.transform_apply(scale=True)