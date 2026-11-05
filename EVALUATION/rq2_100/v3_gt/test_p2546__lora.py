import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

ancho = 1.2
alto = 1.8
profundidad = 0.3
grosor_panel = 0.02

# Paneles laterales
bpy.ops.mesh.primitive_cube_add(location=(-ancho/2 + grosor_panel/2, 0, alto/2))
lateral_izq = bpy.context.active_object
lateral_izq.name = 'Lateral_Izquierdo'
lateral_izq.dimensions = (grosor_panel, profundidad, alto)

bpy.ops.mesh.primitive_cube_add(location=(ancho/2 - grosor_panel/2, 0, alto/2))
lateral_der = bpy.context.active_object
lateral_der.name = 'Lateral_Derecho'
lateral_der.dimensions = (grosor_panel, profundidad, alto)

# Paneles frontales
bpy.ops.mesh.primitive_cube_add(location=(0, -profundidad/2 + grosor_panel/2, alto/2))
frontal_izq = bpy.context.active_object
frontal_izq.name = 'Frontal_Izquierdo'
frontal_izq.dimensions = (ancho - 2 * grosor_panel, grosor_panel, alto)

bpy.ops.mesh.primitive_cube_add(location=(0, profundidad/2 - grosor_panel/2, alto/2))
frontal_der = bpy.context.active_object
frontal_der.name = 'Frontal_Derecho'
frontal_der.dimensions = (ancho - 2 * grosor_panel, grosor_panel, alto)

# Estantes interiores
num_estantes = 4
espacio_entre_estantes = alto / (num_estantes + 1)
for i in range(num_estantes):
    z_pos = i * espacio_entre_estantes + espacio_entre_estantes / 2
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, z_pos))
    estante = bpy.context.active_object
    estante.name = f'Estante_{i+1}'
    estante.dimensions = (ancho - 2 * grosor_panel, profundidad, 0.05)