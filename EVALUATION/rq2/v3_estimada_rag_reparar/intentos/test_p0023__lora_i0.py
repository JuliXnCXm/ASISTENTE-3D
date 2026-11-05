import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
ancho = 0.9
alto = 1.8
fondo = 0.3
grosor_tablero = 0.025
num_estantes = 5

# Crear estantería
A.crear_estanteria(
    nombre="EstanteriaPrincipal",
    ancho=ancho,
    alto=alto,
    fondo=fondo,
    num_estantes=num_estantes,
    grosor_tablero=grosor_tablero,
    origen=(0, 0, 0),
    material="Madera"
)