import bpy

bpy.ops.wm.read_homefile(use_empty=True)

bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

alto_total = 1.8
ancho_total = 0.9
fondo_total = 0.3
espesor_madera = 0.02
num_baldas = 5

def crear_panel(nombre, loc, sca):
    bpy.ops.mesh.primitive_cube_add(location=loc, scale=sca, enter_editmode=False)
    panel = bpy.context.active_object
    panel.name = nombre
    return panel

# Laterales
panel_izq = crear_panel('LateralIzquierdo', (0, (ancho_total / 2) - (espesor_madera / 2), alto_total / 2), (fondo_total, espesor_madera, alto_total))
panel_der = crear_panel('LateralDerecho', (0, -(ancho_total / 2) + (espesor_madera / 2), alto_total / 2), (fondo_total, espesor_madera, alto_total))

# Trasera
panel_trasero = crear_panel('PanelTrasero', ((-fondo_total / 2) + (espesor_madera / 2), 0, alto_total / 2), (espesor_madera, ancho_total, alto_total))

# Baldas
espacio_entre_baldas = (alto_total - espesor_madera) / (num_baldas - 1)
ancho_balda = ancho_total - (2 * espesor_madera)
for i in range(num_baldas):
    z_pos = (i * espacio_entre_baldas) + (espesor_madera / 2)
    if i == 0: # Balda inferior
        z_pos = espesor_madera / 2
    elif i == num_baldas - 1: # Balda superior
        z_pos = alto_total - (espesor_madera / 2)
        
    crear_panel(f'Balda_{i+1}', (0, 0, z_pos), (fondo_total - espesor_madera, ancho_balda, espesor_madera))