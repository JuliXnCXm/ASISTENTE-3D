import bpy

# Configuración inicial
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones generales
ancho_total = 2.2
fondo_total = 0.9
alto_total = 0.7

# Dimensiones de las partes
altura_base = 0.4
ancho_reposabrazos = 0.2
altura_respaldo_sobre_base = alto_total - altura_base
espesor_respaldo = 0.15

ancho_asiento = ancho_total - (2 * ancho_reposabrazos)
fondo_asiento = fondo_total - espesor_respaldo

# Crear base/asiento
bpy.ops.mesh.primitive_cube_add(location=(0, -espesor_respaldo/2, altura_base / 2))
base = bpy.context.active_object
base.name = 'Sofa_Base'
base.dimensions = (ancho_asiento, fondo_asiento, altura_base)

# Crear respaldo
pos_y_respaldo = -fondo_total / 2 + espesor_respaldo / 2
pos_z_respaldo = altura_base + altura_respaldo_sobre_base / 2
bpy.ops.mesh.primitive_cube_add(location=(0, pos_y_respaldo, pos_z_respaldo))
respaldo = bpy.context.active_object
respaldo.name = 'Sofa_Respaldo'
respaldo.dimensions = (ancho_asiento, espesor_respaldo, altura_respaldo_sobre_base)

# Crear reposabrazos
pos_x_reposabrazo = ancho_asiento / 2 + ancho_reposabrazos / 2

# Reposabrazo Derecho
bpy.ops.mesh.primitive_cube_add(location=(pos_x_reposabrazo, 0, alto_total/2))
reposabrazo_d = bpy.context.active_object
reposabrazo_d.name = 'Sofa_Reposabrazo_D'
reposabrazo_d.dimensions = (ancho_reposabrazos, fondo_total, alto_total)

# Reposabrazo Izquierdo
bpy.ops.mesh.primitive_cube_add(location=(-pos_x_reposabrazo, 0, alto_total/2))
reposabrazo_i = bpy.context.active_object
reposabrazo_i.name = 'Sofa_Reposabrazo_I'
reposabrazo_i.dimensions = (ancho_reposabrazos, fondo_total, alto_total)