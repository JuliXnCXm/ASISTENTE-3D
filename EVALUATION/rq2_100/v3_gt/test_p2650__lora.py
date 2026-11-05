import bpy

bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

# Dimensiones
alto_total = 1.8
ancho_total = 1.2
fondo_total = 0.3
num_estantes = 4
grosor_panel = 0.02

# Crear marco exterior
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, alto_total / 2))
marco = bpy.context.active_object
marco.name = 'Estanteria_Marco'
marco.dimensions = (ancho_total + grosor_panel * 2, fondo_total + grosor_panel * 2, alto_total)

# Crear estantes
espacio_util = alto_total - grosor_panel * 2
separacion_z = espacio_util / (num_estantes + 1)
for i in range(num_estantes):
    z_pos = separacion_z * (i + 1) + grosor_panel / 2
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, z_pos)
    )
    estante = bpy.context.active_object
    estante.name = f'Estante_{i+1}'
    estante.dimensions = (ancho_total - grosor_panel * 2, fondo_total, grosor_panel)