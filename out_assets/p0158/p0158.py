import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones generales
ancho_fachada = 12.0
alto_fachada = 9.0
espesor_muro = 0.3

# Dimensiones de ventanas y huecos
ancho_ventana = 2.0
alto_ventana = 1.5
num_ventanas_h = 4
num_ventanas_v = 3
separacion_h = 1.0
separacion_v = 1.0

# Crear paneles verticales (entre ventanas)
ancho_panel_v = separacion_h
for i in range(num_ventanas_h + 1):
    pos_x = -ancho_fachada / 2 + i * (ancho_ventana + separacion_h)
    bpy.ops.mesh.primitive_cube_add(
        location=(pos_x, 0, alto_fachada / 2),
        scale=(ancho_panel_v, espesor_muro, alto_fachada)
    )
    bpy.context.object.name = f"Panel_Vertical_{i}"

# Crear paneles horizontales (dinteles y antepechos)
ancho_panel_h = ancho_ventana
for j in range(num_ventanas_v + 1):
    alto_panel_h = separacion_v
    pos_z = j * (alto_ventana + separacion_v)
    for i in range(num_ventanas_h):
        pos_x = -ancho_fachada / 2 + separacion_h + ancho_ventana/2 + i * (ancho_ventana + separacion_h)
        bpy.ops.mesh.primitive_cube_add(
            location=(pos_x, 0, pos_z),
            scale=(ancho_panel_h, espesor_muro, alto_panel_h)
        )
        bpy.context.object.name = f"Panel_Horizontal_{j}_{i}"