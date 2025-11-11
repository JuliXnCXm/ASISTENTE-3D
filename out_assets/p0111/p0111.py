import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
diametro_esfera = 0.4
radio_esfera = diametro_esfera / 2
altura_suspension = 2.2
longitud_cable = 0.8
radio_cable = 0.01

# Crear la esfera de la lámpara
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=radio_esfera,
    location=(0, 0, altura_suspension)
)

# Crear el cable de suspensión
loc_z_cable = altura_suspension + radio_esfera + (longitud_cable / 2)
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_cable,
    depth=longitud_cable,
    location=(0, 0, loc_z_cable)
)