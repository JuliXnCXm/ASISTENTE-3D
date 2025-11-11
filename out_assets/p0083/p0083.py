import bpy

# Configuración inicial de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones generales
alto = 1.8
ancho = 1.0
fondo = 0.3
espesor_panel = 0.02
num_estantes = 5

# Crear laterales
ancho_util = ancho - (2 * espesor_panel)
pos_x_lateral_1 = -ancho_util / 2 - espesor_panel / 2
pos_x_lateral_2 = ancho_util / 2 + espesor_panel / 2

bpy.ops.mesh.primitive_cube_add(size=1, location=(pos_x_lateral_1, 0, alto / 2))
lateral1 = bpy.context.active_object
lateral1.name = 'Lateral_Izquierdo'
lateral1.dimensions = (espesor_panel, fondo, alto)

bpy.ops.mesh.primitive_cube_add(size=1, location=(pos_x_lateral_2, 0, alto / 2))
lateral2 = bpy.context.active_object
lateral2.name = 'Lateral_Derecho'
lateral2.dimensions = (espesor_panel, fondo, alto)

# Crear estantes
espacio_entre_estantes = alto / (num_estantes -1)

for i in range(num_estantes):
    z_pos = i * espacio_entre_estantes
    # El primer estante al suelo y el ultimo al tope
    if i == 0:
        z_pos = espesor_panel / 2
    elif i == num_estantes -1:
        z_pos = alto - espesor_panel/2
    else:
        z_pos = (alto / (num_estantes-1)) * i - ((alto / (num_estantes-1))/2) + espesor_panel

    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z_pos))
    estante = bpy.context.active_object
    estante.name = f'Estante_{i+1}'
    estante.dimensions = (ancho_util, fondo, espesor_panel)