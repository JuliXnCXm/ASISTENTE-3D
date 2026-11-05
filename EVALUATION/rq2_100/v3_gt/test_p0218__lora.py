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
separacion_centros = 0.80
num_filas = 5
num_columnas = 4

# --- Creación del panel base ---
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto_panel / 2),
    scale=(ancho_panel, espesor_panel, alto_panel)
)
panel_base = bpy.context.active_object
panel_base.name = "Panel_Fachada"

# --- Creación de los objetos de corte (cutter) ---
def crear_cutter(nombre, ubicacion):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radio_perforacion,
        depth=alto_panel * 2, # Asegura que atrape completamente
        location=ubicacion,
        vertices=32 # Para una forma suave
    )
    cutter = bpy.context.active_object
    cutter.name = nombre
    return cutter

# Cálculo de posiciones
pos_x = ancho_panel / num_columnas
pos_y = alto_panel / num_filas
filas = range(num_filas)
columnas = range(num_columnas)

# Bucle para crear cutters
cutters = []
for i in filas:
    for j in columnas:
        x = pos_x * j
        z = pos_y * i + alto_panel / 2
        cutter_loc = (x, 0, z)
        cutter = crear_cutter(f"Cutter_{i}_{j}", cutter_loc)
        cutters.append(cutter)

# --- Aplicar modificador booleano ---
mod = panel_base.modifiers.new(name="Boolean", type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = cutters[0]
bpy.context.view_layer.objects.active = panel_base
bpy.ops.object.modifier_apply(modifier=mod.name)

# --- Limpiar ---
for cutter in cutters:
    bpy.data.objects.remove(cutter, do_unlink=True)