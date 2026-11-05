import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho = 1.2
alto = 1.8
profundidad = 0.3
num_estantes = 5
espesor_panel = 0.02

# Crear panel trasero
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho/2, espesor_panel/2, alto/2))
panel_trasero = bpy.context.active_object
panel_trasero.name = "PanelTrasero"
panel_trasero.scale = (ancho, espesor_panel, alto)

# Crear paneles laterales
loc_izq = (espesor_panel/2, profundidad/2, alto/2)
loc_der = (ancho - espesor_panel/2, profundidad/2, alto/2)
scale_lateral = (espesor_panel, profundidad, alto)

bpy.ops.mesh.primitive_cube_add(size=1, location=loc_izq)
panel_izq = bpy.context.active_object
panel_izq.name = "PanelIzquierdo"
panel_izq.scale = scale_lateral

bpy.ops.mesh.primitive_cube_add(size=1, location=loc_der)
panel_der = bpy.context.active_object
panel_der.name = "PanelDerecho"
panel_der.scale = scale_lateral

# Crear estantes
ancho_interior = ancho - 2 * espesor_panel
espacio_vertical = alto / (num_estantes + 1)
for i in range(num_estantes):
    z_pos = (i + 1) * espacio_vertical
    bpy.ops.mesh.primitive_cube_add(
        size=1, 
        location=(ancho/2, profundidad/2, z_pos))
    estante = bpy.context.active_object
    estante.name = f"Estante_{i+1}"
    estante.scale = (ancho_interior, profundidad, espesor_panel)