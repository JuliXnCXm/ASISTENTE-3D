import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Parámetros de la escalera
num_peldanos = 15
huella = 0.30  # Profundidad del peldaño (en Y)
contrahuella = 0.18 # Altura del peldaño (en Z)
ancho = 1.0 # Ancho del peldaño (en X)

# Crear un objeto padre para la escalera
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
escalera_obj = bpy.context.active_object
escalera_obj.name = "EscaleraRecta"

# Crear cada peldaño en un bucle
for i in range(num_peldanos):
    # Calcular posición del peldaño
    pos_x = 0
    pos_y = i * huella + huella / 2
    pos_z = (i + 1) * contrahuella - contrahuella / 2
    
    # Crear el peldaño (un cubo)
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, pos_y, pos_z)
    )
    peldano = bpy.context.active_object
    peldano.name = f"Peldano_{i+1:02d}"
    
    # Dimensionar el peldaño
    peldano.dimensions = (ancho, huella, contrahuella)
    bpy.ops.object.transform_apply(scale=True)
    
    # Emparentar al objeto principal
    peldano.parent = escalera_obj

# Seleccionar el objeto padre para facilitar la manipulación
bpy.ops.object.select_all(action='DESELECT')
escalera_obj.select_set(True)
bpy.context.view_layer.objects.active = escalera_obj