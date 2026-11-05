import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

def crear_panel(nombre, dimensiones, ubicacion):
    bpy.ops.mesh.primitive_cube_add(location=ubicacion)
    panel = bpy.context.active_object
    panel.name = nombre
    panel.dimensions = dimensiones
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return panel

ancho_estanteria = 1.2
alto_estanteria = 2.0
fondo_estanteria = 0.3
grosor_madera = 0.02
num_baldas = 5

# Paneles laterales
crear_panel('Lateral_Izquierdo', (grosor_madera, fondo_estanteria, alto_estanteria), (-ancho_estanteria/2 + grosor_madera/2, 0, alto_estanteria/2))
crear_panel('Lateral_Derecho', (grosor_madera, fondo_estanteria, alto_estanteria), (ancho_estanteria/2 - grosor_madera/2, 0, alto_estanteria/2))

# Panel trasero
crear_panel('Trasera', (ancho_estanteria - 2*grosor_madera, grosor_madera, alto_estanteria), (0, -fondo_estanteria/2 + grosor_madera/2, alto_estanteria/2))

# Baldas
espacio_entre_baldas = alto_estanteria / (num_baldas + 1)
for i in range(num_baldas):
    altura_balda = (i + 1) * espacio_entre_baldas
    crear_panel(f'Balda_{i+1}', (ancho_estanteria - 2*grosor_madera, fondo_estanteria - grosor_madera, grosor_madera), (0, grosor_madera/2, altura_balda))