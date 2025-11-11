import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configuración de escena
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones
num_peldanos = 12
huella = 0.30  # Profundidad del peldaño (en Y)
contrahuella = 0.17  # Altura del peldaño (en Z)
ancho = 1.2  # Ancho de la escalera (en X)

# Crear un objeto contenedor para la escalera
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
escalera_padre = bpy.context.object
escalera_padre.name = "Escalera"

# Crear cada peldaño en un bucle
for i in range(num_peldanos):
    # Calcular posición del centro de cada peldaño
    loc_x = 0
    loc_y = i * huella + huella / 2
    loc_z = i * contrahuella + contrahuella / 2

    # Crear el cubo para el peldaño
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(loc_x, loc_y, loc_z),
        scale=(ancho / 2, huella / 2, contrahuella / 2)
    )
    peldano = bpy.context.active_object
    peldano.name = f"Peldano_{i+1}"
    peldano.parent = escalera_padre