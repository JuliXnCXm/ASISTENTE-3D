import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho_panel = 1.2
alto_panel = 2.5
grosor_marco = 0.05
profundidad_marco = 0.1
grosor_vidrio = 0.01

# Crear un Empty para agrupar el panel
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
panel_parent = bpy.context.active_object
panel_parent.name = 'PanelMuroCortina'
panel_parent.location.z = alto_panel / 2 # Centrar en su base

# Dimensiones del vidrio
ancho_vidrio = ancho_panel - 2 * grosor_marco
alto_vidrio = alto_panel - 2 * grosor_marco

# Crear panel de vidrio
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, 0),
    scale=(ancho_vidrio / 2, grosor_vidrio / 2, alto_vidrio / 2)
)
vidrio = bpy.context.active_object
vidrio.name = 'Vidrio'
vidrio.parent = panel_parent

# Crear montantes verticales (jambas)
for x_pos in [-ancho_panel/2 + grosor_marco/2, ancho_panel/2 - grosor_marco/2]:
    bpy.ops.mesh.primitive_cube_add(
        location=(x_pos, 0, 0),
        scale=(grosor_marco / 2, profundidad_marco / 2, alto_panel / 2)
    )
    montante_v = bpy.context.active_object
    montante_v.name = 'MontanteVertical'
    montante_v.parent = panel_parent

# Crear travesaños horizontales (dintel y alféizar)
for z_pos in [-alto_panel/2 + grosor_marco/2, alto_panel/2 - grosor_marco/2]:
    bpy.ops.mesh.primitive_cube_add(
        location=(0, 0, z_pos),
        scale=(ancho_vidrio / 2, profundidad_marco / 2, grosor_marco / 2)
    )
    travesano = bpy.context.active_object
    travesano.name = 'TravesanoHorizontal'
    travesano.parent = panel_parent