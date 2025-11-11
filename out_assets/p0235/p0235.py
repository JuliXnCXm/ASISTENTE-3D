import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

altura_poste = 4.0
radio_poste = 0.15 / 2
radio_luminaria = 0.40 / 2

# Crear el poste
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_poste,
    depth=altura_poste,
    location=(0, 0, altura_poste / 2)
)
poste = bpy.context.active_object
poste.name = "PosteDeLuz"

# Crear la luminaria
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=radio_luminaria,
    location=(0, 0, altura_poste + radio_luminaria)
)
luminaria = bpy.context.active_object
luminaria.name = "Luminaria"

# Crear la fuente de luz
bpy.ops.object.light_add(
    type='POINT',
    radius=0.5,
    location=(0, 0, altura_poste + radio_luminaria)
)
luz = bpy.context.active_object
luz.data.energy = 150 # Watts
luz.name = "FuenteDeLuz"