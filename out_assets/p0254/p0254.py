import bpy

# --- Configuración de la escena ---
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# --- Parámetros del banco ---
largo_banco = 1.8
ancho_asiento = 0.45
altura_asiento = 0.4
espesor_liston = 0.04
ancho_liston = 0.1
espacio_liston = 0.02

# --- Creación de soportes de hormigón ---
ancho_soporte = 0.45
alto_soporte = 0.6
grosor_soporte = 0.1
pos_soporte_x = (largo_banco / 2) - grosor_soporte

bpy.ops.mesh.primitive_cube_add(location=(-pos_soporte_x, 0, alto_soporte/2 - 0.2))
soporte_izq = bpy.context.active_object
soporte_izq.name = "SoporteIzquierdo"
soporte_izq.dimensions = (grosor_soporte, ancho_soporte, alto_soporte)

bpy.ops.mesh.primitive_cube_add(location=(pos_soporte_x, 0, alto_soporte/2 - 0.2))
soporte_der = bpy.context.active_object
soporte_der.name = "SoporteDerecho"
soporte_der.dimensions = (grosor_soporte, ancho_soporte, alto_soporte)

# --- Creación de listones del asiento ---
num_listones_asiento = 4
for i in range(num_listones_asiento):
    pos_y = (i * (ancho_liston + espacio_liston)) - (ancho_asiento / 2) + (ancho_liston/2)
    bpy.ops.mesh.primitive_cube_add(
        location=(0, pos_y, altura_asiento + espesor_liston / 2)
    )
    liston = bpy.context.active_object
    liston.name = f"ListonAsiento_{i+1}"
    liston.dimensions = (largo_banco, ancho_liston, espesor_liston)