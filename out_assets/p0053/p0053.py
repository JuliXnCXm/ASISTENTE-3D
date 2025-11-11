import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones generales
ancho = 0.8
alto = 1.8
profundidad = 0.3
espesor_panel = 0.02
num_estantes = 5

# Crear panel lateral izquierdo
bpy.ops.mesh.primitive_cube_add(size=1, location=(espesor_panel/2, profundidad/2, alto/2), scale=(espesor_panel, profundidad, alto))
bpy.context.active_object.name = 'PanelIzquierdo'

# Crear panel lateral derecho
bpy.ops.mesh.primitive_cube_add(size=1, location=(ancho - espesor_panel/2, profundidad/2, alto/2), scale=(espesor_panel, profundidad, alto))
bpy.context.active_object.name = 'PanelDerecho'

# Crear estantes
espacio_entre_estantes = alto / (num_estantes - 1)
for i in range(num_estantes):
    z_pos = i * espacio_entre_estantes
    # El primer y último estante son la base y el tope
    if i == 0:
        z_pos = espesor_panel / 2
    elif i == num_estantes - 1:
        z_pos = alto - espesor_panel / 2
    
    bpy.ops.mesh.primitive_cube_add(
        size=1, 
        location=(ancho/2, profundidad/2, z_pos), 
        scale=(ancho - 2 * espesor_panel, profundidad, espesor_panel)
    )
    bpy.context.active_object.name = f'Estante_{i+1}'