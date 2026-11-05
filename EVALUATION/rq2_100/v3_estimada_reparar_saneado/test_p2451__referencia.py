import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones generales
ancho = 1.2
alto = 1.8
fondo = 0.3
espesor_madera = 0.02
num_baldas = 5

# Crear panel trasero
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho / 2, fondo / 2, alto / 2))
trasera = bpy.context.active_object
trasera.name = 'Panel_Trasero'
trasera.dimensions = (ancho, espesor_madera, alto)

# Crear panel lateral izquierdo
bpy.ops.mesh.primitive_cube_add(size=1, location=(espesor_madera / 2, fondo / 2, alto / 2))
lateral_izq = bpy.context.active_object
lateral_izq.name = 'Panel_Lateral_Izquierdo'
lateral_izq.dimensions = (espesor_madera, fondo, alto)

# Crear panel lateral derecho
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho - espesor_madera / 2, fondo / 2, alto / 2))
lateral_der = bpy.context.active_object
lateral_der.name = 'Panel_Lateral_Derecho'
lateral_der.dimensions = (espesor_madera, fondo, alto)

# Crear baldas
espacio_entre_baldas = alto / (num_baldas + 1)
ancho_interior = ancho - 2 * espesor_madera
for i in range(num_baldas):
    z_pos = (i + 1) * espacio_entre_baldas
    bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho / 2, fondo / 2, z_pos))
    balda = bpy.context.active_object
    balda.name = f'Balda_{i+1}'
    balda.dimensions = (ancho_interior, fondo, espesor_madera)