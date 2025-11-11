import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones del muro
largo = 4.0
alto = 2.5
espesor = 0.15

# Cálculo de la ubicación para que la base esté en Z=0
loc_x = largo / 2
loc_y = espesor / 2
loc_z = alto / 2

# Creación del muro (usando un cubo)
bpy.ops.mesh.primitive_cube_add(
    size=1,
    scale=(largo, espesor, alto),
    location=(loc_x, loc_y, loc_z),
    enter_editmode=False
)