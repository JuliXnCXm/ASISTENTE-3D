import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
liston_largo = 1.8
liston_ancho = 0.08
liston_espesor = 0.04
espacio_listones = 0.02
num_listones = 4
asiento_ancho_total = num_listones * liston_ancho + (num_listones - 1) * espacio_listones

# Crear listones del asiento
for i in range(num_listones):
    loc_x = 0
    loc_y = i * (liston_ancho + espacio_listones) - asiento_ancho_total / 2 + liston_ancho / 2
    loc_z = 0.45
    bpy.ops.mesh.primitive_cube_add(location=(loc_x, loc_y, loc_z))
    liston = bpy.context.active_object
    liston.name = f"Liston.{i+1:03d}"
    liston.dimensions = (liston_largo, liston_ancho, liston_espesor)

# Crear soportes (patas)
ancho_soporte = 0.05
altura_soporte = 0.45
prof_soporte = asiento_ancho_total

posiciones_soportes = [-liston_largo / 2 + 0.15, liston_largo / 2 - 0.15]

for x_pos in posiciones_soportes:
    # Pata vertical
    bpy.ops.mesh.primitive_cube_add(location=(x_pos, 0, altura_soporte / 2))
    pata_v = bpy.context.active_object
    pata_v.dimensions = (ancho_soporte, prof_soporte, altura_soporte)
    pata_v.name = f"SoporteVertical_{x_pos:.2f}"
    # Base horizontal
    bpy.ops.mesh.primitive_cube_add(location=(x_pos, 0, ancho_soporte / 2))
    pata_h = bpy.context.active_object
    pata_h.dimensions = (0.4, prof_soporte, ancho_soporte)
    pata_h.name = f"SoporteHorizontal_{x_pos:.2f}"