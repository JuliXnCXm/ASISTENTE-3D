import bpy
import math

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones
diametro_pantalla = 0.40
radio_pantalla = diametro_pantalla / 2
altura_techo = 3.0
longitud_cable = 1.0
radio_cable = 0.005
diametro_floron = 0.10
altura_floron = 0.03

# Posición inicial
pos_z_pantalla = altura_techo - longitud_cable

# 1. Crear la pantalla semiesférica
bpy.ops.mesh.primitive_uv_sphere_add(
    segments=64,
    ring_count=32,
    radius=radio_pantalla,
    location=(0, 0, pos_z_pantalla)
)
pantalla = bpy.context.active_object
pantalla.name = 'PantallaLampara'

# Usar un booleano para cortar la esfera y hacerla semiesfera
bpy.ops.mesh.primitive_cube_add(
    size=diametro_pantalla * 1.1, 
    location=(0, 0, pos_z_pantalla - radio_pantalla - 0.01)
)
cortador = bpy.context.active_object

mod = pantalla.modifiers.new(name='BooleanCorte', type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = cortador
bpy.context.view_layer.objects.active = pantalla
bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(cortador)

# 2. Crear el cable
bpy.ops.mesh.primitive_cylinder_add(
    radius=radio_cable,
    depth=longitud_cable,
    location=(0, 0, pos_z_pantalla + longitud_cable / 2)
)
bpy.context.active_object.name = 'Cable'

# 3. Crear el florón
bpy.ops.mesh.primitive_cylinder_add(
    radius=diametro_floron / 2,
    depth=altura_floron,
    location=(0, 0, altura_techo - altura_floron / 2)
)
bpy.context.active_object.name = 'Floron'