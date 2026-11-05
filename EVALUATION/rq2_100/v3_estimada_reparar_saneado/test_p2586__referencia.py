import bpy

# Configuración de la escena
bpy.ops.wm.read_homefile(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones generales
ancho = 1.2
alto = 2.0
profundidad = 0.3
grosor_panel = 0.04
num_baldas = 5

# Crear paneles laterales
ancho_interior = ancho - 2 * grosor_panel

# Panel izquierdo
bpy.ops.mesh.primitive_cube_add(size=1, location=(-ancho/2 + grosor_panel/2, 0, alto/2), scale=(grosor_panel, profundidad, alto))
panel_izq = bpy.context.active_object
panel_izq.name = 'Panel_Izquierdo'

# Panel derecho
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho/2 - grosor_panel/2, 0, alto/2), scale=(grosor_panel, profundidad, alto))
panel_der = bpy.context.active_object
panel_der.name = 'Panel_Derecho'

# Crear baldas
espacio_vertical = alto / (num_baldas - 1)
for i in range(num_baldas):
    z_pos = i * espacio_vertical
    # Ajustar la balda superior e inferior para que queden al ras
    if i == 0:
        z_pos = grosor_panel / 2
    elif i == num_baldas - 1:
        z_pos = alto - grosor_panel / 2
    
    bpy.ops.mesh.primitive_cube_add(
        size=1, 
        location=(0, 0, z_pos), 
        scale=(ancho_interior, profundidad, grosor_panel)
    )
    balda = bpy.context.active_object
    balda.name = f'Balda_{i+1}'