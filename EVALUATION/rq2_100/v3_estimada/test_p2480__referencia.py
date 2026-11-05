import bpy

# --- Configuración de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# --- Definición de parámetros
ancho_total = 1.2
altura_total = 1.8
profundidad = 0.3
num_estantes = 5
espesor_panel = 0.02

# --- Crear paneles verticales
ancho_interior = ancho_total - (2 * espesor_panel)

# Panel izquierdo
bpy.ops.mesh.primitive_cube_add(location=(-ancho_total / 2 + espesor_panel / 2, 0, altura_total / 2))
panel_izq = bpy.context.active_object
panel_izq.name = 'Panel_Izquierdo'
panel_izq.dimensions = (espesor_panel, profundidad, altura_total)

# Panel derecho
bpy.ops.mesh.primitive_cube_add(location=(ancho_total / 2 - espesor_panel / 2, 0, altura_total / 2))
panel_der = bpy.context.active_object
panel_der.name = 'Panel_Derecho'
panel_der.dimensions = (espesor_panel, profundidad, altura_total)

# --- Crear estantes
objetos_a_unir = [panel_izq, panel_der]
espacio_entre_estantes = (altura_total - (num_estantes * espesor_panel)) / (num_estantes - 1)

for i in range(num_estantes):
    z_pos = (i * (espacio_entre_estantes + espesor_panel)) + espesor_panel / 2
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, z_pos))
    estante = bpy.context.active_object
    estante.name = f'Estante_{i+1}'
    estante.dimensions = (ancho_interior, profundidad, espesor_panel)
    objetos_a_unir.append(estante)

# --- Unir todas las partes
for obj in bpy.context.scene.objects:
    obj.select_set(False)

for obj in objetos_a_unir:
    obj.select_set(True)

bpy.context.view_layer.objects.active = objetos_a_unir[0]
bpy.ops.object.join()

estanteria = bpy.context.active_object
estanteria.name = 'Estanteria'
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)