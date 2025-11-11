import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones de la mesa
diametro_tablero = 1.2
altura_total = 0.75
espesor_tablero = 0.05
radio_pedestal = 0.15
diametro_base = 0.6
espesor_base = 0.04

# Crear el tablero
radio_tablero = diametro_tablero / 2
loc_z_tablero = altura_total - (espesor_tablero / 2)
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_tablero,
    depth=espesor_tablero,
    location=(0, 0, loc_z_tablero)
)

# Crear el pedestal central
altura_pedestal = altura_total - espesor_tablero - espesor_base
loc_z_pedestal = espesor_base + (altura_pedestal / 2)
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_pedestal,
    depth=altura_pedestal,
    location=(0, 0, loc_z_pedestal)
)

# Crear la base circular
radio_base = diametro_base / 2
loc_z_base = espesor_base / 2
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_base,
    depth=espesor_base,
    location=(0, 0, loc_z_base)
)