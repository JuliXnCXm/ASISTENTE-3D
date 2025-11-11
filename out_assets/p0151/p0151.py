import bpy

# Limpiar la escena para un entorno limpio
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones del banco
largo = 2.0
ancho = 0.5
alto = 0.45

# Crear el cuerpo del banco
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo / 2, ancho / 2, alto / 2),
    scale=(largo, ancho, alto)
)
banco = bpy.context.active_object
banco.name = "BancoHormigon"