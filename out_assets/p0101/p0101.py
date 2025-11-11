import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
long_int = 4.0
anch_int = 3.0
altura = 2.5
espesor_muro = 0.2

# Suelo
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, -espesor_muro/2),
    scale=(long_int + 2 * espesor_muro, anch_int + 2 * espesor_muro, espesor_muro)
)
bpy.context.active_object.name = 'Suelo'

# Muro Norte (+Y)
bpy.ops.mesh.primitive_cube_add(
    location=(0, anch_int/2 + espesor_muro/2, altura/2),
    scale=(long_int + 2 * espesor_muro, espesor_muro, altura)
)
bpy.context.active_object.name = 'MuroNorte'

# Muro Sur (-Y)
bpy.ops.mesh.primitive_cube_add(
    location=(0, -anch_int/2 - espesor_muro/2, altura/2),
    scale=(long_int + 2 * espesor_muro, espesor_muro, altura)
)
bpy.context.active_object.name = 'MuroSur'

# Muro Este (+X)
bpy.ops.mesh.primitive_cube_add(
    location=(long_int/2 + espesor_muro/2, 0, altura/2),
    scale=(espesor_muro, anch_int, altura)
)
bpy.context.active_object.name = 'MuroEste'

# Muro Oeste (-X)
bpy.ops.mesh.primitive_cube_add(
    location=(-long_int/2 - espesor_muro/2, 0, altura/2),
    scale=(espesor_muro, anch_int, altura)
)
bpy.context.active_object.name = 'MuroOeste'