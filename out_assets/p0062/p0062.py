import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

ancho_total = 1.0
alto_total = 2.0
fondo_total = 0.3
espesor_panel = 0.02
num_baldas = 3

def crear_panel(nombre, escala, ubicacion):
    bpy.ops.mesh.primitive_cube_add(size=1, scale=escala, location=ubicacion)
    bpy.context.active_object.name = nombre

ancho_interior = ancho_total - 2 * espesor_panel

# Paneles Verticales
crear_panel('PanelIzquierdo', (espesor_panel, fondo_total, alto_total), (-ancho_total / 2 + espesor_panel / 2, 0, alto_total / 2))
crear_panel('PanelDerecho', (espesor_panel, fondo_total, alto_total), (ancho_total / 2 - espesor_panel / 2, 0, alto_total / 2))

# Base y Tope
crear_panel('PanelBase', (ancho_interior, fondo_total, espesor_panel), (0, 0, espesor_panel / 2))
crear_panel('PanelTope', (ancho_interior, fondo_total, espesor_panel), (0, 0, alto_total - espesor_panel / 2))

# Baldas
altura_util = alto_total - 2 * espesor_panel
espacio_entre_baldas = altura_util / (num_baldas + 1)
for i in range(num_baldas):
    z_pos = (i + 1) * espacio_entre_baldas + espesor_panel / 2
    crear_panel(f'Balda_{i+1}', (ancho_interior, fondo_total, espesor_panel), (0, 0, z_pos))