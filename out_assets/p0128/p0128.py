import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones generales
ancho_total = 0.8
alto_total = 1.8
profundidad_total = 0.3
num_estantes = 5
espesor_madera = 0.02

# Crear paneles laterales
ancho_panel_lateral = espesor_madera
alto_panel_lateral = alto_total
prof_panel_lateral = profundidad_total

pos_x_izq = -ancho_total / 2 + espesor_madera / 2
pos_x_der = ancho_total / 2 - espesor_madera / 2

bpy.ops.mesh.primitive_cube_add(location=(pos_x_izq, 0, alto_total / 2), scale=(ancho_panel_lateral, prof_panel_lateral, alto_panel_lateral))
bpy.context.object.name = "PanelIzquierdo"

bpy.ops.mesh.primitive_cube_add(location=(pos_x_der, 0, alto_total / 2), scale=(ancho_panel_lateral, prof_panel_lateral, alto_panel_lateral))
bpy.context.object.name = "PanelDerecho"

# Crear estantes
ancho_estante = ancho_total - (2 * espesor_madera)
alto_estante = espesor_madera
prof_estante = profundidad_total

espacio_entre_estantes = alto_total / (num_estantes -1)

for i in range(num_estantes):
    altura_estante = i * espacio_entre_estantes
    # El último estante va arriba del todo
    if i == num_estantes -1 :
        altura_estante = alto_total - espesor_madera/2
    # El primer estante va abajo del todo
    if i == 0:
        altura_estante = espesor_madera/2

    bpy.ops.mesh.primitive_cube_add(location=(0, 0, altura_estante), scale=(ancho_estante, prof_estante, alto_estante))
    bpy.context.object.name = f"Estante_{i+1}"