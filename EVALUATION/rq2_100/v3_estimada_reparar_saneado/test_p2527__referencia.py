import bpy

# --- CONFIGURACIÓN DE LA ESCENA ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# --- PARÁMETROS DE LA ESTANTERÍA ---
ancho_total = 1.2
alto_total = 2.0
profundidad_total = 0.3
espesor_madera = 0.02
numero_baldas = 5

# --- CREACIÓN DE COMPONENTES ---
# Panel trasero
bpy.ops.mesh.primitive_cube_add(location=(0, profundidad_total/2 - espesor_madera/2, alto_total/2))
panel_trasero = bpy.context.active_object
panel_trasero.name = 'Panel_Trasero'
panel_trasero.dimensions = (ancho_total, espesor_madera, alto_total)

# Panel lateral izquierdo
bpy.ops.mesh.primitive_cube_add(location=(-ancho_total/2 + espesor_madera/2, 0, alto_total/2))
panel_izquierdo = bpy.context.active_object
panel_izquierdo.name = 'Panel_Izquierdo'
panel_izquierdo.dimensions = (espesor_madera, profundidad_total, alto_total)

# Panel lateral derecho
bpy.ops.mesh.primitive_cube_add(location=(ancho_total/2 - espesor_madera/2, 0, alto_total/2))
panel_derecho = bpy.context.active_object
panel_derecho.name = 'Panel_Derecho'
panel_derecho.dimensions = (espesor_madera, profundidad_total, alto_total)

# Baldas
ancho_balda = ancho_total - (2 * espesor_madera)
profundidad_balda = profundidad_total - espesor_madera
espacio_entre_baldas = alto_total / (numero_baldas + 1)

for i in range(numero_baldas):
    altura_balda = (i + 1) * espacio_entre_baldas
    bpy.ops.mesh.primitive_cube_add(location=(0, -espesor_madera/2, altura_balda))
    balda = bpy.context.active_object
    balda.name = f'Balda_{i+1}'
    balda.dimensions = (ancho_balda, profundidad_balda, espesor_madera)