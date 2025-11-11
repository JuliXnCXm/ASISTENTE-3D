import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones y posición
diametro = 0.4
altura_lampara = 0.15
altura_suspension = 2.5

radio = diametro / 2
pos_z = altura_suspension

# Crear el cuerpo de la lámpara
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio,
    depth=altura_lampara,
    location=(0, 0, pos_z),
    vertices=64
)

lampa_cuerpo = bpy.context.object
lampa_cuerpo.name = "CuerpoLamparaCilindrica"

# Opcional: Crear un punto de luz en el centro
bpy.ops.object.light_add(
    type='POINT',
    radius=0.1,
    location=(0, 0, pos_z - altura_lampara / 2)
)
luz = bpy.context.object
luz.name = "LuzLampara"
luz.data.energy = 50 # Watts