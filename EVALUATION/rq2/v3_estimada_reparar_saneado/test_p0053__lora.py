import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
alto_total = 1.8
ancho_total = 0.8
profundidad_total = 0.3
num_estantes = 5
grosor_panel = 0.02

# Crear panel trasero
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, alto_total / 2),
    scale=(ancho_total, profundidad_total, alto_total)
)
panel_trasero = bpy.context.active_object
panel_trasero.name = "PanelTrasero"
bpy.ops.object.transform_apply(scale=True)

# Crear estantes
espacio_entre_estantes = alto_total / (num_estantes + 1)
for i in range(num_estantes):
    z_pos = i * espacio_entre_estantes + (espacio_entre_estantes / 2)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos),
        scale=(ancho_total, profundidad_total, grosor_panel)
    )
    estante = bpy.context.active_object
    estante.name = f"Estante_{i+1}"
    bpy.ops.object.transform_apply(scale=True)