import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# --- Configuración
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros
altura_poste = 4.0
diametro_poste = 0.15
lado_luminaria = 0.30

# --- Crear el poste
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_poste / 2,
    depth=altura_poste,
    location=(0, 0, altura_poste / 2)
)
poste = bpy.context.active_object
poste.name = "PosteDeLuz"

# --- Crear la luminaria
bpy.ops.mesh.primitive_cube_add(
    size=lado_luminaria,
    location=(0, 0, altura_poste - lado_luminaria / 2)
)
luminaria = bpy.context.active_object
luminaria.name = "Luminaria"

# --- Crear la fuente de luz
luz_data = bpy.data.lights.new(name="LuzPoste", type='POINT')
luz_data.energy = 50 # Watts
luz_objeto = bpy.data.objects.new(name="FuenteDeLuz", object_data=luz_data)
scene.collection.objects.link(luz_objeto)
luz_objeto.location = (0, 0, altura_poste - lado_luminaria / 2)