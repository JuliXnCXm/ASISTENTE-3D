import bpy

# Configuración inicial
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
altura_poste = 4.0
diametro_poste = 0.15
tam_luminaria = 0.3

# Crear el poste cilíndrico
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_poste / 2,
    depth=altura_poste,
    location=(0, 0, altura_poste / 2)
)
poste = bpy.context.active_object
poste.name = "PosteLuz"

# Crear la luminaria cúbica
pos_z_lum = altura_poste + tam_luminaria / 2
bpy.ops.mesh.primitive_cube_add(
    size=tam_luminaria,
    location=(0, 0, pos_z_lum)
)
luminaria = bpy.context.active_object
luminaria.name = "Luminaria"

# Crear la fuente de luz
bpy.ops.object.light_add(
    type='POINT',
    radius=0.5,
    location=(0, 0, altura_poste + tam_luminaria * 0.4)
)
luz = bpy.context.active_object
luz.data.energy = 200 # Potencia en Watts
luz.name = "FuenteLuz"