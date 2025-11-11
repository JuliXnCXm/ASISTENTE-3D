import bpy

bpy.ops.wm.read_homefile(use_empty=True)

# Configurar unidades a metros
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.length_unit = 'METERS'

# Dimensiones del puf
diametro = 0.80
alto = 0.45
radio = diametro / 2

# Crear el puf usando un cilindro
bpy.ops.mesh.primitive_cylinder_add(
    vertices=64,
    radius=radio,
    depth=alto,
    location=(0, 0, alto / 2)
)

# Renombrar y suavizar
puf = bpy.context.active_object
puf.name = 'PufCilindrico'

# Añadir modificador de bisel para bordes suaves sin entrar a modo edición
bvel_mod = puf.modifiers.new(name='Bisel', type='BEVEL')
bvel_mod.width = 0.02
bvel_mod.segments = 5

# Sombrado suave
shade_smooth_op = getattr(bpy.ops.object, 'shade_smooth', None)
if shade_smooth_op:
    shade_smooth_op()