import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
alto_total = 1.8
ancho_total = 0.8
profundidad_total = 0.3
num_estantes = 5
grosor_panel = 0.02

# Crear marco exterior
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, alto_total / 2))
marco = bpy.context.active_object
marco.name = 'Estanteria_Marco'
marco.dimensions = (ancho_total, profundidad_total, alto_total)

# Crear estantes interiores
espacio_util = alto_total - grosor_panel * num_estantes
separacion_z = espacio_util / (num_estantes - 1) if num_estantes > 1 else 0

for i in range(num_estantes):
    z_pos = grosor_panel + separacion_z * i
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z_pos))
    estante = bpy.context.active_object
    estante.name = f'Estante_{i+1}'
    estante.dimensions = (ancho_total - grosor_panel * 2, profundidad_total - grosor_panel * 2, grosor_panel)