import bpy

bpy.ops.wm.read_homefile(use_empty=True)

scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

altura_poste = 4.0
radio_poste = 0.075
largo_brazo = 1.0
seccion_brazo = 0.1
tamano_luminaria = 0.3

# Crear el poste
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_poste,
    depth=altura_poste,
    location=(0, 0, altura_poste / 2)
)
poste = bpy.context.active_object
poste.name = 'PosteFarola'

# Crear el brazo horizontal
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(largo_brazo / 2, 0, altura_poste - seccion_brazo / 2),
    scale=(largo_brazo, seccion_brazo, seccion_brazo)
)
brazo = bpy.context.active_object
brazo.name = 'BrazoFarola'

# Crear la luminaria
bpy.ops.mesh.primitive_cube_add(
    size=tamano_luminaria,
    location=(largo_brazo, 0, altura_poste - seccion_brazo - tamano_luminaria / 2)
)
luminaria = bpy.context.active_object
luminaria.name = 'Luminaria'