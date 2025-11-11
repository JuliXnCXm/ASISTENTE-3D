import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros de la farola ---
altura_poste = 4.0
radio_poste = 0.1
tamano_luminaria = 0.4

# --- Crear poste ---
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_poste,
    depth=altura_poste,
    location=(0, 0, altura_poste / 2)
)
poste = bpy.context.active_object
poste.name = "PosteFarola"

# --- Crear luminaria ---
bpy.ops.mesh.primitive_cube_add(
    size=tamano_luminaria,
    location=(0, 0, altura_poste + tamano_luminaria / 2)
)
luminaria = bpy.context.active_object
luminaria.name = "Luminaria"

# --- Crear fuente de luz ---
bpy.ops.object.light_add(
    type='POINT',
    radius=1,
    location=(0, 0, altura_poste + 0.1)
)
luz = bpy.context.active_object
luz.data.energy = 150 # Watts
luz.name = "LuzFarola"