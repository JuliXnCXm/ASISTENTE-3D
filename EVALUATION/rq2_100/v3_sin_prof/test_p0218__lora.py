import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del panel ---
ancho_panel = 3.0
alto_panel = 5.0
espesor_panel = 0.2
radio_perforacion = 0.20
espacio_centros = 0.80

# --- Crear el panel base ---
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto_panel / 2),
    scale=(ancho_panel, espesor_panel, alto_panel)
)
panel_base = bpy.context.active_object
panel_base.name = "Panel_Fachada"

# --- Crear el objeto para perforar ---
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_perforacion,
    depth=alto_panel * 2,
    location=(0, 0, alto_panel),
    vertices=64
)
cutter = bpy.context.active_object
cutter.name = "Cutter_Perforacion"
cutter.display_type = 'WIRE'

# --- Aplicar modificador booleano ---
mod_bool = panel_base.modifiers.new(name="BooleanPerforacion", type='BOOLEAN')
mod_bool.operation = 'DIFFERENCE'
mod_bool.object = cutter

# --- Aplicar y limpiar ---
bpy.context.view_layer.objects.active = panel_base
bpy.ops.object.modifier_apply(modifier=mod_bool.name)

# --- Eliminar el objeto de corte ---
bpy.data.objects.remove(cutter)