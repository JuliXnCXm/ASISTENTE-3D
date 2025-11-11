import bpy

# Limpiar la escena
bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'METERS'

# Dimensiones del asiento
asiento_largo = 2.0
asiento_ancho = 0.45
asiento_espesor = 0.10
altura_asiento = 0.40

# Dimensiones del soporte
soporte_lado = 0.35
soporte_altura = altura_asiento

# Crear el asiento
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, altura_asiento + asiento_espesor / 2)
)
asiento = bpy.context.active_object
asiento.name = 'AsientoBanco'
asiento.dimensions = (asiento_largo, asiento_ancho, asiento_espesor)

# Calcular posición de los soportes
distancia_soporte = (asiento_largo / 2) - (soporte_lado / 2) - 0.1

# Crear primer soporte
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(-distancia_soporte, 0, soporte_altura / 2)
)
soporte1 = bpy.context.active_object
soporte1.name = 'SoporteBanco.001'
soporte1.dimensions = (soporte_lado, asiento_ancho, soporte_altura)

# Crear segundo soporte
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(distancia_soporte, 0, soporte_altura / 2)
)
soporte2 = bpy.context.active_object
soporte2.name = 'SoporteBanco.002'
soporte2.dimensions = (soporte_lado, asiento_ancho, soporte_altura)