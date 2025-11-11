import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
altura_poste = 4.0
radio_poste = 0.08
largo_brazo = 1.5
dimension_brazo = 0.1
tamano_luminaria = 0.3

# Crear poste vertical
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_poste,
    depth=altura_poste,
    location=(0, 0, altura_poste / 2)
)
bpy.context.object.name = 'Poste_Luz'

# Crear brazo horizontal
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_brazo / 2, 0, altura_poste - dimension_brazo / 2),
    scale=(largo_brazo, dimension_brazo, dimension_brazo)
)
bpy.context.object.name = 'Brazo_Luz'

# Crear luminaria
bpy.ops.mesh.primitive_cube_add(
    size=tamano_luminaria,
    location=(largo_brazo - tamano_luminaria/2, 0, altura_poste - dimension_brazo - tamano_luminaria/2)
)
bpy.context.object.name = 'Luminaria'