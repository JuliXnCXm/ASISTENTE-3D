import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# --- Configuración de la escena
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Dimensiones del banco
largo = 2.0
ancho = 0.5
alto = 0.45

# --- Creación del banco
bpy.ops.mesh.primitive_cube_add(
    size=1,
    enter_editmode=False,
    align='WORLD',
    location=(largo / 2, ancho / 2, alto / 2)
)
banco = bpy.context.active_object
banco.name = 'BancoDeHormigon'

# --- Aplicar dimensiones
banco.dimensions = (largo, ancho, alto)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)