import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

ancho = 1.2
alto = 1.8
profundidad = 0.3
espesor_panel = 0.02
num_estantes = 5

def crear_panel(nombre, escala, ubicacion):
    bpy.ops.mesh.primitive_cube_add(size=1, location=ubicacion)
    panel = bpy.context.active_object
    panel.name = nombre
    panel.scale = escala
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return panel

# Panel trasero
crear_panel("Panel_Trasero", (ancho, espesor_panel, alto), (0, profundidad/2 - espesor_panel/2, alto/2))

# Panel lateral izquierdo
crear_panel("Panel_Izquierdo", (espesor_panel, profundidad, alto), (-ancho/2 + espesor_panel/2, 0, alto/2))

# Panel lateral derecho
crear_panel("Panel_Derecho", (espesor_panel, profundidad, alto), (ancho/2 - espesor_panel/2, 0, alto/2))

# Estantes
ancho_interior = ancho - 2 * espesor_panel
espacio_vertical = alto / (num_estantes + 1)

for i in range(num_estantes):
    z = (i + 1) * espacio_vertical
    crear_panel(f"Estante_{i+1}", (ancho_interior, profundidad, espesor_panel), (0, 0, z))