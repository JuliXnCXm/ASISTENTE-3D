import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Parámetros de la escalera
num_peldanos = 15
ancho = 1.0
huella = 0.30 # Profundidad en Y
contrahuella = 0.18 # Altura en Z

# Crear cada peldaño en un bucle
for i in range(num_peldanos):
    # Calcular la posición de cada peldaño
    pos_x = 0
    pos_y = i * huella + huella / 2
    pos_z = i * contrahuella + contrahuella / 2

    # Crear el cubo para el peldaño
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(pos_x, pos_y, pos_z)
    )
    
    # Ajustar las dimensiones del peldaño
    peldano = bpy.context.object
    peldano.dimensions = (ancho, huella, contrahuella)
    peldano.name = f"Peldano_{i+1:02d}"