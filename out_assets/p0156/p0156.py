import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho_total = 4.0
profundidad_total = 2.0
altura_paneles = 2.2
espesor_techo = 0.1
espesor_vidrio = 0.02
profundidad_lateral = 1.0

# Crear el techo
bpy.ops.mesh.primitive_cube_add(
    location=(0, (profundidad_total - profundidad_lateral)/2, altura_paneles + espesor_techo / 2),
    scale=(ancho_total, profundidad_total, espesor_techo)
)
techo = bpy.context.active_object
techo.name = "Marquesina_Techo"

# Crear panel trasero
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, altura_paneles / 2),
    scale=(ancho_total, espesor_vidrio, altura_paneles)
)
panel_trasero = bpy.context.active_object
panel_trasero.name = "Marquesina_PanelTrasero"

# Crear panel lateral izquierdo
bpy.ops.mesh.primitive_cube_add(
    location=(-ancho_total / 2, profundidad_lateral / 2, altura_paneles / 2),
    scale=(espesor_vidrio, profundidad_lateral, altura_paneles)
)
panel_izq = bpy.context.active_object
panel_izq.name = "Marquesina_PanelIzquierdo"

# Crear panel lateral derecho
bpy.ops.mesh.primitive_cube_add(
    location=(ancho_total / 2, profundidad_lateral / 2, altura_paneles / 2),
    scale=(espesor_vidrio, profundidad_lateral, altura_paneles)
)
panel_der = bpy.context.active_object
panel_der.name = "Marquesina_PanelDerecho"