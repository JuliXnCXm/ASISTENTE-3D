import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones de los peldaños
num_peldanos = 15
ancho = 1.0
huella = 0.30       # Profundidad en Y
contrahuella = 0.18 # Altura en Z

# Crear un objeto Empty como padre de la escalera
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
escalera_parent = bpy.context.active_object
escalera_parent.name = 'EscaleraRecta'

# Bucle para crear cada peldaño
for i in range(num_peldanos):
    # Calcular posición del peldaño
    pos_x = 0
    pos_y = i * huella + huella / 2
    pos_z = i * contrahuella + contrahuella / 2
    
    # Crear el peldaño (cubo)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, pos_y, pos_z),
        scale=(ancho, huella, contrahuella)
    )
    peldano = bpy.context.active_object
    peldano.name = f'Peldano_{i+1}'
    
    # Emparentar el peldaño al objeto Empty
    peldano.parent = escalera_parent

# Seleccionar el objeto padre para facilitar la manipulación
bpy.ops.object.select_all(action='DESELECT')
escalera_parent.select_set(True)
bpy.context.view_layer.objects.active = escalera_parent