import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# --- Configuración
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# --- Parámetros
numero_bolardos = 3
altura = 1.0
diametro = 0.3
separacion = 1.2 # Distancia entre centros

# --- Bucle de creación
for i in range(numero_bolardos):
    # Calcular la posición X para cada bolardo
    pos_x = i * separacion
    
    # Crear el cilindro (bolardo)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=diametro / 2,
        depth=altura,
        location=(pos_x, 0, altura / 2)
    )
    bolardo = bpy.context.active_object
    bolardo.name = f"Bolardo_{i+1}"

# --- Centrar el conjunto de bolardos en el origen
pos_central_x = ((numero_bolardos - 1) * separacion) / 2
for obj in scene.objects:
    if obj.name.startswith("Bolardo"):
        obj.location.x -= pos_central_x