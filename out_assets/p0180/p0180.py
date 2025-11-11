import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Parámetros de la escalera
num_peldanos = 15
ancho_peldano = 1.2
huella = 0.3 # Profundidad del peldaño (eje Y)
contrahuella = 0.17 # Altura del peldaño (eje Z)

# Crear un objeto padre para la escalera
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
escalera_padre = bpy.context.active_object
escalera_padre.name = "EscaleraRecta"

# Crear los peldaños en un bucle
for i in range(num_peldanos):
    # Calcular la posición de cada peldaño
    # El centro del peldaño se desplaza en Y y Z
    pos_x = 0
    pos_y = i * huella + huella / 2
    pos_z = i * contrahuella + contrahuella / 2
    
    # Crear el cubo que representará el peldaño
    bpy.ops.mesh.primitive_cube_add(
        size=1, 
        location=(pos_x, pos_y, pos_z)
    )
    
    peldano = bpy.context.active_object
    peldano.name = f"Peldano_{i+1:02d}"
    
    # Escalar el cubo a las dimensiones correctas
    peldano.scale = (ancho_peldano, huella, contrahuella)
    
    # Emparentar el peldaño al objeto padre
    peldano.parent = escalera_padre

# Seleccionar y aplicar transformaciones a todos los peldaños
for obj in bpy.context.scene.objects:
    if obj.name.startswith("Peldano_"):
        obj.select_set(True)

bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
bpy.ops.object.select_all(action='DESELECT')
escalera_padre.select_set(True)
bpy.context.view_layer.objects.active = escalera_padre