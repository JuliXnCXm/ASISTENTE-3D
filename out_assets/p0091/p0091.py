import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones generales
alto_total = 1.8
ancho_total = 1.0
fondo_total = 0.3
espesor_panel = 0.02
num_baldas = 5

def crear_panel(nombre, escala, posicion):
    bpy.ops.mesh.primitive_cube_add(size=1, scale=escala, location=posicion)
    panel = bpy.context.active_object
    panel.name = nombre
    return panel

# Paneles laterales
escala_lateral = (espesor_panel, fondo_total, alto_total)
crear_panel('PanelIzquierdo', escala_lateral, (-(ancho_total / 2) + espesor_panel / 2, 0, alto_total / 2))
crear_panel('PanelDerecho', escala_lateral, ((ancho_total / 2) - espesor_panel / 2, 0, alto_total / 2))

# Baldas
espacio_entre_baldas = alto_total / (num_baldas - 1)
ancho_balda = ancho_total - (2 * espesor_panel)
escala_balda = (ancho_balda, fondo_total, espesor_panel)

for i in range(num_baldas):
    z_pos = (i * espacio_entre_baldas) + espesor_panel / 2
    # La balda inferior y superior son especiales para que queden al ras
    if i == 0:
        z_pos = espesor_panel / 2
    elif i == num_baldas - 1:
        z_pos = alto_total - espesor_panel / 2
    else:
        # Recalcular para baldas intermedias
        espacio_util = alto_total - espesor_panel*2
        num_espacios_intermedios = num_baldas - 1
        z_pos = espesor_panel + (i * espacio_util / num_espacios_intermedios) - espesor_panel/2

    crear_panel(f'Balda_{i+1}', escala_balda, (0, 0, z_pos))