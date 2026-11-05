import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros ---
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

# --- Crear los objetos de corte (cutter) ---
num_filas = int(alto_panel / espacio_centros) + 1
num_columnas = int(ancho_panel / espacio_centros) + 1

for fila in range(num_filas):
    for col in range(num_columnas):
        x_pos = -ancho_panel/2 + (col * espacio_centros) + espacio_centros/2
        z_pos = -alto_panel/2 + (fila * espacio_centros) + espacio_centros/2
        
        bpy.ops.mesh.primitive_cylinder_add(
            radius=radio_perforacion,
            depth=alto_panel,
            location=(x_pos, 0, z_pos)
        )
        cutter = bpy.context.active_object
        cutter.name = f"Cutter_{fila}_{col}"
        
        # Aplicar modificador booleano
        bool_mod = panel_base.modifiers.new(name=f"Boolean_{fila}_{col}", type='BOOLEAN')
        bool_mod.operation = 'DIFFERENCE'
        bool_mod.object = cutter
        bpy.context.view_layer.objects.active = panel_base
        bpy.ops.object.modifier_apply(modifier=bool_mod.name)

        # Eliminar el cutter
        bpy.data.objects.remove(cutter, do_unlink=True)