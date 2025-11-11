import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Dimensiones
longitud_cable = 1.0
diametro_pantalla = 0.30
radio_pantalla = diametro_pantalla / 2
radio_cable = 0.005 # 5mm

# Posición central en el techo (asumimos un techo a 2.5m)
altura_techo = 2.5

# Crear el cable (cilindro)
bpy.ops.mesh.primitive_cylinder_add(
    vertices=16,
    radius=radio_cable,
    depth=longitud_cable,
    location=(0, 0, altura_techo - longitud_cable / 2)
)
cable = bpy.context.active_object
cable.name = "CableLampara"

# Crear la pantalla (esfera)
pos_z_pantalla = altura_techo - longitud_cable - radio_pantalla
bpy.ops.mesh.primitive_uv_sphere_add(
    segments=32,
    ring_count=16,
    radius=radio_pantalla,
    location=(0, 0, pos_z_pantalla)
)
pantalla = bpy.context.active_object
pantalla.name = "PantallaEsferica"

# Crear fuente de luz puntual
bpy.ops.object.light_add(
    type='POINT',
    radius=0.1,
    location=(0, 0, pos_z_pantalla)
)
luz = bpy.context.active_object
luz.data.energy = 50 # Watts